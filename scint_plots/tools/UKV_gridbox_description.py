# Beth Saunders 27/02/2023

# imports
import numpy as np


def get_MORUSES_params(furb=1):
    """
    MORUSES parameters (wrr,hgt,hwr) from land-use fraction
    see Bohnenstengel et al. 2011;  equations copied from MORUSES-JULES code
    Original script from Denise: email on 23/02/23
    :param furb: fraction of total urban (roof + canyon)
    :return:
    """

    # Equation 3 Sylvia paper
    lambdap = 22.878 * furb ** 6 - 59.473 * furb ** 5 + 57.749 * furb ** 4 - 25.108 * furb ** 3 + 4.3337 * furb ** 2 + 0.1926 * furb + 0.036
    # Equation 4 Sylvia paper
    lambdaf = 16.412 * furb ** 6 - 41.855 * furb ** 5 + 40.387 * furb ** 4 - 17.759 * furb ** 3 + 3.2399 * furb ** 2 + 0.0626 * furb + 0.0271

    # Mean building height
    hgt = 167.409 * furb ** 5 - 337.853 * furb ** 4 + 247.813 * furb ** 3 - 76.3678 * furb ** 2 + 11.4832 * furb + 4.48226

    # Height to width ratio
    # page 4 Sylvia paper: in text
    hwr = np.pi / 2.0 * lambdaf / (1.0 - lambdap)

    # canyon width ratio (road fraction)
    # page 4 Sylvia paper: in text
    wrr = 1.0 - lambdap

    return {'wrr': wrr, 'hwr': hwr, 'hgt': hgt}


if __name__ == '__main__':

    # dict of urban fractions in eacg gridbox
    # from Table in SM
    # furb_dict = {1: 0.9282, 2: 0.8959, 3: 0.7891}
    furb_dict = {1: 0.8959, 2: 0.9282, 3: 0.9381, 4: 0.7891, 5: 0.7897, 6: 0.6908}

    for gridbox in furb_dict.keys():
        MORUSES_dict = get_MORUSES_params(furb=furb_dict[gridbox])

        print(' ')
        print('Gridbox: ', gridbox)
        print('H/W: ', MORUSES_dict['hwr'])
        print('W/R: ', MORUSES_dict['wrr'])
        print('z_h: ', MORUSES_dict['hgt'])

    print('end')
