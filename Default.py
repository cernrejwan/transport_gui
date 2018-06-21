default_values = {
    '--t0': 0,
    '-S': 0,
    '-a': 5,
    '-p': 8,

    'EAR1': {
        'const': '-D Z -t 40 -x 0.0 -y 0.0 -z 41.06',
        '-L': 185,
        'collimation': ['ear1', 'ear1_5cm', 'ear1_capture_2011', 'ear1misalign', 'ear1fission', 'ear1fission_misalign']
    },

    'EAR2': {
        'const': '-D Y -t 16 -x -10.8 -y 37.2 -z 9.86',
        '-L': 19.5,
        'collimation': ['ear2', 'ear2_misalign', 'ear2_misalign_fission', 'ear2_misalign_20cmCorr',
                        'ear2_misalign_2015', 'ear2_misalign_revised2018']
    },

    'shape': {
        'circular': {
            '-r': 0,
            '-R': 1.65,
            '-s': 0.05
        },
        'rectangular': {
            '--x1': -1,
            '--x2': 1,
            '--y1': -1,
            '--y2': 1
        }
    },

    'histogram': {
        '1D': ['Energy [eV]', 'Tof [s]'],
        '2D': ['Tof [s] vs Energy [eV]', 'Lambda [cm] vs Energy [eV]', 'Lambda [cm] vs Tof [s]', 'Profile [cm] vs [cm]'],
        'num_iters': 50,
        '-T': 'e',
        '-h': '1e-3',
        '-H': '1e9',
        '-b': -2,
        '-B': 2,
        '-n': 6000,
        '-m': 6000,
    },

    'cross_section': {
        'path': '/afs/cern.ch/user/n/ntofsimu/public/transport/totalXS/',
        'materials': {'Mylar': {'density': 1.36, 'molecular_mass': 192.13, 'formula': [('H', 0.041959), ('C', 0.625016), ('O', 0.333025)]},
                      'Kapton': {'density': 1.42, 'molecular_mass': 382.27, 'formula': [('H', 0.026362), ('C', 0.691133), ('N', 0.07327), ('O', 0.209235)]}}
    }
}
