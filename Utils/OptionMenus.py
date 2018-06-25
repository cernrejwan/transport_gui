histogram_types = {
    '1D': ['Energy [eV]', 'Tof [s]'],
    '2D': ['Tof [s] vs Energy [eV]', 'Lambda [cm] vs Energy [eV]', 'Lambda [cm] vs Tof [s]', 'Profile [cm] vs [cm]']
}

support_materials = {
    'Mylar': {'density': 1.36,
              'formula': [('H', 0.041959, 'Natural'), ('C', 0.625016, 'Natural'), ('O', 0.333025, 'Natural')]},
    'Kapton': {'density': 1.42,
               'formula': [('H', 0.026362, 'Natural'), ('C', 0.691133, 'Natural'),
                           ('N', 0.07327, 'Natural'), ('O', 0.209235, 'Natural')]}
}
