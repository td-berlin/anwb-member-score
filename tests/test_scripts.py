# %% IMPORTS

from anwb_member_score import scripts

# %% FUNCTIONS

def test_main() -> None:
    # given
    argv = ["x", "y", "z"]
    # when
    result = scripts.main(argv)
    # then
    assert result == 0, "Result should be 0!"
