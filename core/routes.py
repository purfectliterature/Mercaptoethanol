ROOT = "https://coursemology.org"
LOGIN = "/users/sign_in"
COURSE = "/courses/{}"
ASSESSMENTS = "/assessments"
SUBMISSIONS = "/submissions"
MATERIALS = "/materials"
FOLDERS = "/folders"

def login(): return ROOT + LOGIN

def course(id): return ROOT + COURSE.format(id)    

def assessments(id): return course(id) + ASSESSMENTS

def download(id, mid): return assessments(id) + "/" + mid + SUBMISSIONS + "/download_all?format=json"

def workbin(id, wid): return course(id) + MATERIALS + FOLDERS + "/" + str(wid)
