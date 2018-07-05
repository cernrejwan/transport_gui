from BasePage import *
import subprocess


class SubmitPage(BasePage):
    def __init__(self, parent, controller, iters, **kwargs):
        BasePage.__init__(self, parent, controller, "Submission", has_prev=False)
        Label(self.frame, text="Submitting {0} jobs to HTCondor".format(iters), justify=LEFT).pack()
        self.job_ids = list()

    def get_next_button(self):
        return 'Exit', self.controller.destroy

    def submit(self, cmd, iters, work_dir, ear):
        submit_dir, jobs_dir, output_dir = self.make_submit_dir(work_dir)
        input_files = self.controller.get_input_files()
        transport_code = self.controller.paths['transport_simulation_code']

        for i in range(iters):
            job_file = os.path.join(submit_dir, 'jobs', 'job_{0}.sh'.format(i))
            input_file = os.path.join(input_files[i], ear + '.bin')
            output_file = os.path.join(output_dir, 'res_' + str(i))
            primeries = self.get_primeries(input_files[i])
            if not primeries:
                Label(self.frame, text="Problem with job_{0}. Skipping.".format(i), justify=LEFT).pack()
                self.frame.update()
                continue

            full_cmd = transport_code + ' -d ' + input_file + ' -o ' + output_file + '-P ' + str(primeries) + cmd
            with open(job_file, 'w') as f:
                f.write(full_cmd)

            os.system('./HTCondorSub.sh ' + job_file)
            self.job_ids.append(subprocess.Popen(['condor_submit', job_file + '.CondorSub.sh'],
                                                 stdout=subprocess.PIPE).communicate()[0])

            Label(self.frame, text="job_{0} submitted successfully.".format(i), justify=LEFT).pack()
            self.frame.update()

        Label(self.frame, text="Done!", justify=LEFT).pack()
        self.frame.update()

        with open(os.path.join(submit_dir, 'job_ids.txt'), 'w') as f:
            f.writelines(self.job_ids)

    def make_submit_dir(self, work_dir):
        submit_dir = os.path.join(work_dir, "submit")
        if os.path.exists(submit_dir):
            ls = os.listdir(work_dir)
            ls = [int(f.split('_')[1]) for f in ls if f.startswith('submit_')]
            idx = '2' if not ls else max(ls) + 1
            submit_dir = os.path.join(work_dir, 'submit_' + str(idx))
            self.controller.raise_error_message(
                "'submit' folder already exists in output directory.\nCreating folder 'submit_{0}' instead.".format(idx), title='Warning')

        os.mkdir(submit_dir)
        jobs_dir = os.path.join(submit_dir, 'jobs')
        os.mkdir(jobs_dir)
        output_dir = os.path.join(submit_dir, 'output')
        os.mkdir(output_dir)
        return submit_dir, jobs_dir, output_dir

    def get_primeries(self, path):
        info_file = os.path.join(path, 'info')
        if not os.path.exists(info_file):
            self.controller.raise_error_message('Info file does not exist in dir {0}. Skipping.'.format(path))
            return
        with open(info_file, 'r') as f:
            data = f.readlines()
        primaries = [i for i in data if i.startswith("primaries")][0]
        num = primaries.split(' ')[1]
        return num
