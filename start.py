from core.project import Project
from core.session import Session

session = Session()

# Authentication needs only be done once. To improve processing time, next
# time running the script, comment out the following line. Session will
# automatically scan if there is a need for reauthentication. If so, will
# raise an exception.
if (session.is_valid()):
    session.authenticate(input("Email: ").strip(), input("Password :"))

# First time running, use the following expression
# project = Project.of(session, <job_name>, <course_id>)
# for example: Project.of(session, "cs1010s-1920s2", 1821)
#
# If project.mproj is present, or you want to transfer job from previous
# batch, just use Project.load(). It will scan and process the preexisting
# project.mproj.
project = Project.load()#Project.of(session, "meth-alpha", 1821)

# If starting anew, the following command will delete permanently(!) dumps,
# submissions, logs, templates, and session cookies. Will need to re-login.
project.reset()

# The following command will export and save the current Project into
# project.mproj. Next time, can just load the Project instead of creating a
# new Project.
project.export()

# The following command will download all submissions from all missions in
# the course. The list of missions is stored in project.mproj.
project.dump_all(session)

# The following command will unpack all downloaded zips into submissions.
project.unpack()

# The following command will download templates from course's workbin.
project.get_templates(session)

# The following command will upload all submissions with their templates to
# moss with parameters: ./moss -l python -m 50 -b <template> <files>
# Optional first argument: ignore missions with the filters given 
# (e.g. ignores contests).
# Optional second argument: output json filename containing the MOSS URLs
project.upload_to_moss("contest", "moss.json")

