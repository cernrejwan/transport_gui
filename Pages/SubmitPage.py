from BasePage import *
import subprocess


template = '''#! /bin/tcsh
if ($?LS_SUBCWD) then
  set locdir=`pwd`
  set destdir=$LS_SUBCWD
else
  set locdir=/tmp/$USER
  set destdir={output_dir}/
  mkdir -p $locdir 
  cd $locdir 
endif

echo Copying Input File
cp {input_file}  $locdir/.
ls -lh
echo Start of Transport
{transport} -d  $locdir/{ear}.bin -o  $locdir/res_{i}.hist -P {primaries} {cmd}   
echo Start of Transport
ls -lh
echo Moving Output File to Destination
xrdcp  $locdir/res_{i}.hist $destdir/.
ls -lh
echo This is the End.
'''


class SubmitPage(BasePage):
    def __init__(self, parent, controller, iters, submit_dir, **kwargs):
        BasePage.__init__(self, parent, controller, "Submission", has_prev=False)
        Label(self.frame, text="Creating submit directory:", justify=LEFT).pack()
        text_dir = Text(self.frame, height=1, width=45)
        text_dir.insert(INSERT, submit_dir)
        text_dir.pack()
        Label(self.frame, text="Submitting {0} job(s) to HTCondor".format(iters), justify=LEFT).pack()
        self.frame.update()
        self.job_ids = list()

    def get_next_button(self):
        return 'Exit', self.controller.exit_window

    def submit(self, cmd, iters, submit_dir, ear):
        output_dir = os.path.join(submit_dir, 'output')
        input_files = self.controller.get_input_files()
        transport_code = self.controller.paths['transport_simulation_code']

        for i in range(iters):
            job_file = os.path.join(submit_dir, 'jobs', 'job_{0}.sh'.format(i))
            input_file = os.path.join(input_files[i], ear + '.bin')

            primaries = self.get_primaries(input_files[i])
            if not primaries:
                self.controller.raise_error_message('Info file does not exist in dir {0}.\nSkipping.'.format(input_files[i]))
                Label(self.frame, text="Problem with job_{0}. Skipping.".format(i), justify=LEFT).pack()
                self.frame.update()
                continue

            with open(job_file, 'w') as f:
                f.write(template.format(ear=ear, i=i, transport=transport_code, input_file=input_file,
                                        output_dir=output_dir, primaries=primaries, cmd=cmd))

            os.system(self.controller.paths['HTCondorSub'] + ' ' + job_file)
            out = subprocess.Popen(['condor_submit', job_file + '.CondorSub.sh'], stdout=subprocess.PIPE).communicate()[0]
            job_id = (out.split(' ')[-1]).split('.')[0]
            self.job_ids.append(job_id)

            Label(self.frame, text="job_{0} submitted successfully.".format(i), justify=LEFT).pack()
            self.frame.update()

        Label(self.frame, text="Done!", justify=LEFT).pack()
        self.frame.update()

        with open(os.path.join(submit_dir, 'jobs', 'job_ids.txt'), 'w') as f:
            f.write('\n'.join(self.job_ids))

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
