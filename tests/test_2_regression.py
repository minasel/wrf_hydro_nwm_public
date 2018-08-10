import pickle

import pytest
import wrfhydropy


#regression question
def test_regression_data(output_dir, capsys):
    with capsys.disabled():
        print("\nQuestion: The candidate run data values match the reference run?", end="")

    # Check for existence of sim objects
    candidate_run_file = output_dir / 'run_candidate' / 'WrfHydroSim_collected.pkl'
    reference_run_file = output_dir / 'run_reference' / 'WrfHydroSim_collected.pkl'

    if candidate_run_file.is_file() is False:
        pytest.skip('Candidate run object not found, skipping test')
    if reference_run_file.is_file() is False:
        pytest.skip('Reference run object not found, skipping test')

    # Load run objects
    candidate_run_expected = pickle.load(candidate_run_file.open(mode="rb"))
    reference_run_expected = pickle.load(reference_run_file.open(mode="rb"))

    #Check regression
    data_diffs = wrfhydropy.outputdiffs.OutputDataDiffs(candidate_run_expected.output,
                                               reference_run_expected.output)

    # Assert all diff values are 0 and print diff stats if not
    has_data_diffs = any(value != 0 for value in data_diffs.diff_counts.values())
    if has_data_diffs:
        with capsys.disabled():
            print(data_diffs.diff_counts)
        for key, value in data_diffs.diff_counts.items():
            if value != 0:
                with capsys.disabled():
                    print('\n' + key + '\n')
                    print(getattr(data_diffs, key))
    assert has_data_diffs == False, \
        'Data values in outputs for candidate run do not match reference run'

#regression question
def test_regression_metadata(output_dir, capsys):
    with capsys.disabled():
        print("\nQuestion: The candidate run output metadata match the reference run?",
              end="")

    # Check for existence of sim objects
    candidate_run_file = output_dir / 'run_candidate' / 'WrfHydroSim_collected.pkl'
    reference_run_file = output_dir / 'run_reference' / 'WrfHydroSim_collected.pkl'

    if candidate_run_file.is_file() is False:
        pytest.skip('Candidate run object not found, skipping test')
    if reference_run_file.is_file() is False:
        pytest.skip('Reference run object not found, skipping test')

    # Load run objects
    candidate_run_expected = pickle.load(candidate_run_file.open(mode="rb"))
    reference_run_expected = pickle.load(reference_run_file.open(mode="rb"))

    #Check regression
    meta_data_diffs = wrfhydropy.outputdiffs.OutputMetaDataDiffs(candidate_run_expected.output,
                                               reference_run_expected.output)

    # Assert all diff values are 0 and print diff stats if not
    has_data_diffs = any(value != 0 for value in meta_data_diffs.diff_counts.values())
    if has_data_diffs:
        with capsys.disabled():
            print(meta_data_diffs.diff_counts)
        for key, value in meta_data_diffs.diff_counts.items():
            if value != 0:
                with capsys.disabled():
                    print('\n' + key + '\n')
                    print(getattr(meta_data_diffs, key))
    assert has_data_diffs == False, \
        'Metadata and attributes in outputs for candidate run do not match reference run'