from BasePage import *


class SubmitPage(BasePage):
    def __init__(self, parent, controller, iters, **kwargs):
        BasePage.__init__(self, parent, controller, "Submission", has_prev=False)
        Label(self.frame, text="Submitting {0} jobs to HTCondor".format(iters), justify=LEFT).pack()

    def get_next_button(self):
        return 'Exit', self.controller.destroy

    def submit(self, cmd, iters, output_dir, ear):
        submit_dir = self.get_submit_dir(output_dir)
        os.mkdir(submit_dir)

        input_files = self.controller.get_input_dirs()

        for i in range(iters):
            job_file = os.path.join(submit_dir, 'job_{0}.sh'.format(i))
            input_file = os.path.join(input_files[i], ear, '.bin')
            out = self.get_full_cmd(self.controller.paths['transport_simulation_code'], submit_dir, input_file, cmd, i)

            with open(job_file, 'w') as f:
                f.write(out)
            os.system('./HTCondorSub.sh ' + job_file)
            os.system('condor_submit ' + job_file + '.CondorSub.sh')
            Label(self.frame, text="Job #{0} submitted successfully".format(i), justify=LEFT).pack()

    def get_submit_dir(self, output_dir):
        result = os.path.join(output_dir, "submit")
        if os.path.exists(result):
            ls = os.listdir(output_dir)
            ls = [int(f.split('_')[1]) for f in ls if f.startswith('submit_')]
            idx = '2' if not ls else max(ls) + 1
            result = os.path.join(output_dir, 'submit_' + str(idx))
            self.controller.raise_error_message(
                "'submit' folder already exists in output directory.\nCreating folder 'submit_{0}' instead.".format(idx))
        return result

    @staticmethod
    def get_full_cmd(transport_simulation_code, submit_dir, input_file, cmd, i):
        output_file = os.path.join(submit_dir, 'res_' + str(i))
        return transport_simulation_code + ' -d ' + input_file + ' -o ' + output_file + cmd
