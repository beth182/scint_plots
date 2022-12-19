import scint_fp.functions.sa_lc_fractions.lc_fractions_in_sa as lc


def create_lc_fractions_in_sa_csv(doy_choice,
                                  av_period,
                                  file_list,
                                  save_path):
    """
    Creates a csv file of landcover fractions present in all the target SA files.
    :return:
    """

    # construct csv file path
    csv_file_name = str(doy_choice) + '_' + av_period + '.csv'
    csv_file_path = save_path + csv_file_name

    # run the sa lc function from scint_fp
    sas_df = lc.lc_fract_multiple_sas(sa_list=file_list, save_path=save_path)

    # save the df as a csv
    sas_df.to_csv(csv_file_path)

    return sas_df
