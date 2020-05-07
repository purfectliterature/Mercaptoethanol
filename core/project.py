import os
import time
import datetime
import zipfile
import shutil
import string
import core.assessment as assessment
import core.cooljson as cooljson
import core.routes as routes
import core.parser as parser
from core.session import Session

class Project:
    PATH_TO_PROCESS = "core/process.sh"
    PATH_TO_MOSS = "core/moss"
    MOSS_PARAMS = "-l python -m 50"
    DEFAULT_FILE_NAME = "project.mproj"
    DEFAULT_DOWNLOADS = "dumps"
    DEFAULT_SUBMISSIONS = "submissions"
    DEFAULT_TEMPLATES = "templates"
    DEFAULT_LOGS = "logs"
    DEFAULT_MOSS_OUTPUT = "moss.json"
    FIELD_PROJECT_NAME = "project_name"
    FIELD_COURSE_ID = "course_id"
    FIELD_COURSE_TITLE = "course_title"
    FIELD_MISSIONS = "missions"
    FIELD_WORKBIN = "workbin"
    VALID_FIELDS = [
        FIELD_PROJECT_NAME,
        FIELD_COURSE_ID,
        FIELD_COURSE_TITLE,
        FIELD_MISSIONS,
        FIELD_WORKBIN
    ]
    ERR_FIELD_NOT_FOUND = "field {} not found, invalid project file"
    CHECK_INTERVAL = 1
    TIMEOUT_TRIES = 60
    valid_chars = list()
    valid_chars.extend(string.ascii_letters)
    valid_chars.extend(string.digits)
    valid_chars.extend(" .!-'\",_&()+")

    @staticmethod
    def prepare_dir(name):
        if (not os.path.exists(name)):
            os.mkdir(name)
        return True

    @staticmethod
    def check_empty_dir(name):
        if (os.path.exists(name)):
            return len(os.listdir(name)) == 0
        return True

    @staticmethod
    def load(filename=DEFAULT_FILE_NAME):
        read_dict = cooljson.read_json(filename)
        for field in Project.VALID_FIELDS:
            if (not read_dict.get(field, None)): raise ValueError(Project.ERR_FIELD_NOT_FOUND.format(field))
        return Project(read_dict)

    @staticmethod
    def to_dict(name, course_id, course_title, missions, workbin):
        return {
            Project.FIELD_PROJECT_NAME: name,
            Project.FIELD_COURSE_ID: course_id,
            Project.FIELD_COURSE_TITLE: course_title,
            Project.FIELD_MISSIONS: missions,
            Project.FIELD_WORKBIN: workbin
        }

    @staticmethod
    def of(session, name, id):
        res = session.get(routes.course(id))
        course_title = parser.find(res, ["li", {"class": "active"}]).contents[0]
        workbin = list(filter(lambda y: False if not y else routes.MATERIALS.split("/")[-1] in y, [x.get("href") for x in parser.select(res, "ul.nav li a")]))[0].split("/")[-1]
        res = session.get(routes.assessments(id))
        assessments = parser.select(res, "tr.assessment th a")
        return Project(Project.to_dict(name, id, course_title, dict((x.get("href").split("/")[-1], x.string) for x in assessments), workbin))

    @staticmethod
    def download(session, url, path):
        res = session.get(url)
        if (len(res) == 0): return False # no submissions
        job_url = routes.ROOT + cooljson.parse_json(res).get("redirect_url", None) + "?format=json"
        counter = 0
        while counter < Project.TIMEOUT_TRIES:
            res = session.get(job_url)
            data = cooljson.parse_json(res)
            status = data.get("status", None)
            download_url = None
            if (status == "completed"):
                download_url = data.get("redirect_url")
                break
            time.sleep(Project.CHECK_INTERVAL)
            counter += 1
        return Session.download(routes.ROOT + download_url, path)

    @staticmethod
    def reset():
        def r(path):
            if (os.path.exists(path)): shutil.rmtree(path)
        r(Project.DEFAULT_DOWNLOADS)
        r(Project.DEFAULT_LOGS)
        r(Project.DEFAULT_SUBMISSIONS)
        r(Project.DEFAULT_TEMPLATES)
        if (os.path.exists(Session.DEFAULT_COOKIES_FILE)):
            os.remove(Session.DEFAULT_COOKIES_FILE)
        return True

    @staticmethod
    def slugify(text):
        output = ""
        for char in text:
            if (char not in Project.valid_chars):
                output += " "
            else:
                output += char
        return output
    
    def __init__(self, meta):
        self.name = meta.get(Project.FIELD_PROJECT_NAME, None)
        self.course_id = meta.get(Project.FIELD_COURSE_ID, None)
        self.course_title = meta.get(Project.FIELD_COURSE_TITLE, None)
        self.missions = list(assessment.Assessment(x[0], x[1]) for x in meta.get(Project.FIELD_MISSIONS, None).items())
        self.workbin = meta.get(Project.FIELD_WORKBIN)

    def __str__(self):
        return f"<Project {self.name} for {self.course_id} {self.course_title} with {list(map(str, self.missions))}>"

    def export(self):
        cooljson.write_json(Project.DEFAULT_FILE_NAME, Project.to_dict(
            self.name,
            self.course_id,
            self.course_title,
            dict(x.to_pair() for x in self.missions),
            self.workbin
        ))
        return True

    def dump_mission(self, session, mission):
        if (Project.prepare_dir(Project.DEFAULT_DOWNLOADS)):
            return Project.download(session, routes.download(self.course_id, mission.id), Project.DEFAULT_DOWNLOADS + "/" + Project.slugify(mission.filename()))
        else:
            raise Exception("Dumps not found")
        
    def dump_all(self, session):
        if (Project.prepare_dir(Project.DEFAULT_DOWNLOADS)):
            for mission in self.missions:
                if (self.dump_mission(session, mission)):
                    print("Dumped " + mission.title)
                else:
                    print("No submissions for " + mission.title)
            return True
        else:
            raise Exception("Directory not empty")

    def unpack(self):
        if (not Project.check_empty_dir(Project.DEFAULT_DOWNLOADS)):
            dumps_list = os.listdir(Project.DEFAULT_DOWNLOADS)
            zips_list = list(filter(lambda x: ".zip" in x, dumps_list))
            for zip_name in zips_list:
                zip_file = Project.DEFAULT_DOWNLOADS + "/" + zip_name
                os.system("./" + Project.PATH_TO_PROCESS + " \"" + zip_file + "\" " + str(self.course_id))

            if (Project.check_empty_dir(Project.DEFAULT_SUBMISSIONS)):
                if (Project.prepare_dir(Project.DEFAULT_SUBMISSIONS)):
                    dumps_list = os.listdir(Project.DEFAULT_DOWNLOADS)
                    unpacked_list = list(filter(lambda x: ".zip" not in x, dumps_list))
                    for unpacked_name in unpacked_list:
                        unpacked_src = Project.DEFAULT_DOWNLOADS + "/" + unpacked_name
                        unpacked_dest = Project.DEFAULT_SUBMISSIONS + "/" + unpacked_name
                        os.system("mv \"" + unpacked_src + "\" \"" + unpacked_dest + "\"")
                        print("Unpacked " + unpacked_name)
                else:
                    raise Exception("Submissions not found")
            else:
                raise Exception("Submissions not empty")
        else:
            raise Exception("Dumps not found")

    def get_templates(self, session):
        NAME = "missions"
        res = session.get(routes.workbin(self.course_id, self.workbin))
        # missions_tail may induce IndexError if "missions" not in x.text.lower()!
        missions_folder = list(filter(lambda x: NAME in x.text.lower(), parser.select(res, "tr.material_folder td a")))[0].get("href").split("/")[-1]
        if (Project.download(session, routes.workbin(self.course_id, missions_folder) + "/download?format=json", NAME + ".zip")):
            if (Project.prepare_dir(Project.DEFAULT_TEMPLATES)):
                with zipfile.ZipFile(NAME + ".zip", 'r') as zip_ref:
                    zip_ref.extractall(Project.DEFAULT_TEMPLATES)
                if (os.path.exists(NAME + ".zip")): os.remove(NAME + ".zip")

    def upload_to_moss(self, blacklist=None, filename=Project.DEFAULT_MOSS_OUTPUT):
        now = datetime.datetime.now()
        timestamp = f"{str(now.date())}-{str(now.time().hour)}-{str(now.time().minute)}-{str(now.time().second)}"
        submissions = os.listdir(Project.DEFAULT_SUBMISSIONS)
        templates = os.listdir(Project.DEFAULT_TEMPLATES)
        pairs = dict()
        for submission in submissions:
            if (submission in templates):
                pairs[submission] = list(filter(lambda x: "template.py" in x.lower(), os.listdir(Project.DEFAULT_TEMPLATES + "/" + submission)))[0]

        moss_links = dict()
        
        if (Project.prepare_dir(Project.DEFAULT_LOGS)):
            for submission, template in pairs.items():
                if (blacklist and blacklist.lower() in submission.lower()): continue
                submission_path = Project.DEFAULT_SUBMISSIONS + "/" + submission
                template_path = Project.DEFAULT_TEMPLATES + "/" + submission + "/" + template
                logs_path = Project.DEFAULT_LOGS + "/uptm-" + timestamp + "_" + submission + ".mlog"
                command = f"./{Project.PATH_TO_MOSS} {Project.MOSS_PARAMS} -b \"{template_path}\" \"{submission_path}\"/* >> \"{logs_path}\""
                os.system(command)

                print("Uploaded " + submission + " to moss")

                with open(logs_path, "r") as log:
                    moss_link = list(log)[-1][:-1]
                    moss_links[submission] = moss_link
                    print(moss_link + "\n")

        return cooljson.write_json(filename, moss_links)
