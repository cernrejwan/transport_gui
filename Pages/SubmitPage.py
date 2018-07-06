from BasePage import *
import subprocess
import time
from datetime import datetime


class SubmitPage(BasePage):
    def __init__(self, parent, controller, iters, **kwargs):
        BasePage.__init__(self, parent, controller, "Submission", has_prev=False)
        Label(self.frame, text="Submitting {0} jobs to HTCondor".format(iters), justify=LEFT).pack()
        self.job_ids = list()

    def get_next_button(self):
        return 'Exit', self.controller.destroy

    def submit(self, cmd, iters, work_dir, ear):
        submit_dir, jobs_dir, output_dir = self.make_submit_dir(work_dir)
        save_path = os.path.join(submit_dir, 'configs.csv')
        self.controller.save_configs(save_path)

        input_files = self.controller.get_input_files()
        transport_code = self.controller.paths['transport_simulation_code']

        for i in range(iters):
            job_file = os.path.join(submit_dir, 'jobs', 'job_{0}.sh'.format(i))
            input_file = os.path.join(input_files[i], ear + '.bin')
            output_file = os.path.join(output_dir, 'res_' + str(i))

            primaries = self.get_primaries(input_files[i])
            if not primaries:
                self.controller.raise_error_message('Info file does not exist in dir {0}.\nSkipping.'.format(input_files[i]))
                Label(self.frame, text="Problem with job_{0}. Skipping.".format(i), justify=LEFT).pack()
                self.frame.update()
                continue

            full_cmd = transport_code + ' -d ' + input_file + ' -o ' + output_file + '-P ' + str(primaries) + ' ' + cmd
            with open(job_file, 'w') as f:
                f.write(full_cmd)

            os.system('./HTCondorSub.sh ' + job_file)
            out = subprocess.Popen(['condor_submit', job_file + '.CondorSub.sh'], stdout=subprocess.PIPE).communicate()[0]
            job_id = (out.split(' ')[-1])[:-1]
            self.job_ids.append(job_id)

            Label(self.frame, text="job_{0} submitted successfully.".format(i), justify=LEFT).pack()
            self.frame.update()

        Label(self.frame, text="Done!", justify=LEFT).pack()
        self.frame.update()

        with open(os.path.join(submit_dir, 'job_ids.txt'), 'w') as f:
            f.writelines(self.job_ids)

    @staticmethod
    def make_submit_dir(work_dir):
        timestamp = datetime.fromtimestamp(time.time()).strftime('%y%m%d_%H%M%S')
        submit_dir = os.path.join(work_dir, "submit_" + timestamp)

        os.mkdir(submit_dir)
        jobs_dir = os.path.join(submit_dir, 'jobs')
        os.mkdir(jobs_dir)
        output_dir = os.path.join(submit_dir, 'output')
        os.mkdir(output_dir)
        return submit_dir, jobs_dir, output_dir

    @staticmethod
    def get_primaries(path):
        info_file = os.path.join(path, 'info')
        if not os.path.exists(info_file):
            return
        with open(info_file, 'r') as f:
            data = f.readlines()
        primaries = [i for i in data if i.startswith("primaries")][0]
        num = primaries.split(' ')[1]
        return num
