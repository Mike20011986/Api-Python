class TestLenPhrase:
    def test_len_prase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) < 15, "The phrase is not less than 15 symbols"