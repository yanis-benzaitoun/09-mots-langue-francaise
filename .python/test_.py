import sys
import os
import pytest
import tempfile
from unittest.mock import patch, mock_open
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import read_data, ensemble_mots, mots_de_n_lettres, mots_avec, cherche1, cherche2

FILENAME = "corpus.txt"


@pytest.fixture(scope="module")
def corpus_data():
    """Fixture to load corpus data once for all tests."""
    if os.path.exists(FILENAME):
        return read_data(FILENAME)
    else:
        pytest.skip(f"Corpus file {FILENAME} not found")


@pytest.fixture(scope="module")
def corpus_set():
    """Fixture to load corpus as a set once for all tests."""
    if os.path.exists(FILENAME):
        return ensemble_mots(FILENAME)
    else:
        pytest.skip(f"Corpus file {FILENAME} not found")


class TestReadData:
    """Test class for the read_data function with corpus.txt focus."""
    
    def test_read_data_corpus_file_basic(self, corpus_data):
        """Test that read_data can read the corpus.txt file."""
        result = corpus_data
        assert isinstance(result, list)
        assert len(result) > 0
        # Based on the doctest in main.py, we expect 336531 words
        assert len(result) == 336531
    
    def test_read_data_corpus_specific_words(self, corpus_data):
        """Test specific words from corpus.txt based on doctest examples."""
        result = corpus_data
        # Test specific indices from the doctest in main.py
        assert result[1] == 'à'
        assert result[328570] == 'vaincre'
        assert result[290761] == 'sans'
        assert result[233574] == 'péril'
        assert result[221712] == 'on'
        assert result[324539] == 'triomphe'
        assert result[166128] == 'gloire'
    
    def test_read_data_corpus_first_and_last_words(self, corpus_data):
        """Test the first and last words in corpus.txt."""
        result = corpus_data
        # First word should be 'a'
        assert result[0] == 'a'
        # Last word should not be empty
        assert result[-1] != ''
        assert len(result[-1]) > 0
    
    def test_read_data_corpus_no_empty_strings(self, corpus_data):
        """Test that corpus.txt doesn't contain empty strings."""
        result = corpus_data
        # Check that there are no empty strings in the corpus
        empty_count = sum(1 for word in result if word == '')
        assert empty_count == 0, f"Found {empty_count} empty strings in corpus"
    
    def test_read_data_corpus_no_newlines_in_words(self, corpus_data):
        """Test that words in corpus.txt don't contain newlines."""
        result = corpus_data
        # Check a sample of words for newlines
        sample_size = min(1000, len(result))
        for i in range(0, len(result), len(result) // sample_size):
            word = result[i]
            assert '\n' not in word, f"Found newline in word at index {i}: '{word}'"
            assert '\r' not in word, f"Found carriage return in word at index {i}: '{word}'"
    
    def test_read_data_corpus_unicode_support(self, corpus_data):
        """Test that corpus.txt handles French unicode characters correctly."""
        result = corpus_data
        # Test that 'à' is properly handled (from doctest)
        assert 'à' in result
        # Look for other French characters in a sample
        french_chars = set('àâäéèêëïîôöùûüÿñç')
        found_french = False
        for word in result[:10000]:  # Check first 10000 words
            if any(char in french_chars for char in word):
                found_french = True
                break
        assert found_french, "No French characters found in sample"
    
    def test_read_data_return_type_and_structure(self, corpus_data):
        """Test that read_data returns the correct type and structure."""
        result = corpus_data
        assert isinstance(result, list)
        # All elements should be strings
        assert all(isinstance(word, str) for word in result[:100])
    
    def test_read_data_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_data("non_existent_file.txt")
    
    def test_read_data_with_mock_simple(self):
        """Test read_data using mocking for controlled input."""
        mock_content = "hello\nworld\ntest\n"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            result = read_data("mock_file.txt")
            expected = ['hello', 'world', 'test']
            assert result == expected
    
    def test_read_data_with_mock_empty_lines(self):
        """Test read_data with empty lines using mocking."""
        mock_content = "hello\n\nworld\n"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            result = read_data("mock_file.txt")
            expected = ['hello', '', 'world']
            assert result == expected
    
    def test_read_data_with_mock_whitespace(self):
        """Test read_data strips whitespace correctly using mocking."""
        mock_content = "  hello  \n\t world \t\n  python\n"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            result = read_data("mock_file.txt")
            expected = ['hello', 'world', 'python']
            assert result == expected
    
    def test_read_data_with_mock_unicode(self):
        """Test read_data with unicode characters using mocking."""
        mock_content = "café\nnaïve\nà\n"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            result = read_data("mock_file.txt")
            expected = ['café', 'naïve', 'à']
            assert result == expected
    
    def test_read_data_with_temporary_file(self):
        """Test read_data with a real temporary file."""
        test_content = "hello\nworld\npython\ntest\n"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf8') as f:
            f.write(test_content)
            temp_filename = f.name
        
        try:
            result = read_data(temp_filename)
            expected = ['hello', 'world', 'python', 'test']
            assert result == expected
            assert len(result) == 4
        finally:
            os.unlink(temp_filename)
    
    def test_read_data_empty_file(self):
        """Test read_data with an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf8') as f:
            temp_filename = f.name
        
        try:
            result = read_data(temp_filename)
            assert result == []
            assert isinstance(result, list)
        finally:
            os.unlink(temp_filename)
    
    def test_read_data_single_word_file(self):
        """Test read_data with a file containing one word."""
        test_content = "single\n"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf8') as f:
            f.write(test_content)
            temp_filename = f.name
        
        try:
            result = read_data(temp_filename)
            assert result == ['single']
            assert len(result) == 1
        finally:
            os.unlink(temp_filename)
    
    def test_read_data_corpus_consistency(self, corpus_data):
        """Test that read_data produces consistent results when called multiple times."""
        result1 = corpus_data
        result2 = read_data(FILENAME)  # Call again to test consistency
        assert result1 == result2
        assert len(result1) == len(result2)
    
    def test_read_data_corpus_sample_words_exist(self, corpus_data):
        """Test that expected French words exist in the corpus."""
        result = corpus_data
        result_set = set(result)
        # Test some common French words that should be in the corpus
        expected_words = ['le', 'de', 'et', 'à', 'un', 'être', 'avoir']
        for word in expected_words:
            assert word in result_set, f"Expected word '{word}' not found in corpus"


class TestEnsembleMots:
    """Test class for the ensemble_mots function."""
    
    def test_ensemble_mots_corpus_basic(self, corpus_set):
        """Test that ensemble_mots returns a set with correct properties."""
        result = corpus_set
        assert isinstance(result, set)
        assert len(result) > 0
        # Based on the doctest in main.py, we expect 336531 words
        assert len(result) == 336531
    
    def test_ensemble_mots_contains_specific_words(self, corpus_set):
        """Test specific words from corpus based on doctest examples."""
        result = corpus_set
        # Test from the doctest
        assert "glomérules" in result
        assert "glycosudrique" not in result
        
        # Additional specific French words that should be in the corpus
        assert "anticonstitutionnellement" in result  # One of the longest French words
        assert "constitutionnalisassent" in result    # From main.py doctest examples
        assert "hospitalo-universitaires" in result   # From main.py doctest examples
        assert "oto-rhino-laryngologiste" in result   # From main.py doctest examples
        
        # Common French words with accents
        assert "être" in result
        assert "avoir" in result
        assert "français" in result
        assert "déjà" in result
        assert "très" in result
        assert "où" in result
        
        # Words that should NOT be in a French corpus
        assert "nonexistentword123" not in result
        assert "fakefrenchword" not in result
        assert "zzzzzzzzz" not in result
        assert "" not in result  # Empty string should not be in the set
        
        # Test some technical/scientific terms
        assert "algorithme" in result
        assert "programmation" in result
        assert "ordinateur" in result
        
        # Test some short words
        assert "a" in result
        assert "à" in result
        assert "je" in result
        assert "tu" in result
        assert "il" in result
        assert "le" in result
        assert "la" in result
        assert "un" in result
        assert "de" in result
        assert "et" in result
    
    def test_ensemble_mots_no_duplicates(self, corpus_set, corpus_data):
        """Test that ensemble_mots removes duplicates compared to read_data."""
        set_result = corpus_set
        list_result = corpus_data
        
        # Set should have no duplicates
        assert len(set_result) == len(set(list_result))
        
        # All words from the list should be in the set
        for word in list_result:
            assert word in set_result
    
  
    def test_ensemble_mots_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            ensemble_mots("non_existent_file.txt")
    
    
    def test_ensemble_mots_consistency(self, corpus_set):
        """Test that ensemble_mots produces consistent results when called multiple times."""
        result1 = corpus_set
        result2 = ensemble_mots(FILENAME)  # Call again to test consistency
        assert result1 == result2
        assert len(result1) == len(result2)
    
    def test_ensemble_mots_set_operations(self, corpus_set):
        """Test that the result supports set operations."""
        result = corpus_set
        
        # Test set intersection
        sample_words = {'le', 'de', 'et', 'non_existent_word'}
        intersection = result & sample_words
        assert 'le' in intersection
        assert 'de' in intersection
        assert 'et' in intersection
        assert 'non_existent_word' not in intersection
        
        # Test set membership
        assert 'à' in result  # From doctest
        assert 'glomérules' in result  # From doctest
        assert 'glycosudrique' not in result  # From doctest
    
    def test_ensemble_mots_comparison_with_read_data(self, corpus_set, corpus_data):
        """Test the relationship between ensemble_mots and read_data results."""
        set_result = corpus_set
        list_result = corpus_data
        
        # Set should contain all unique elements from the list
        assert set_result == set(list_result)
        
        # Length comparison (set removes duplicates)
        assert len(set_result) <= len(list_result)
        
        # Check that conversion works both ways
        assert set(list_result) == set_result
        assert sorted(list(set_result)) == sorted(list(set(list_result)))


class TestMotsDeNLettres:
    """Test class for the mots_de_n_lettres function."""
    
    def test_mots_de_n_lettres_corpus_basic(self, corpus_set):
        """Test basic functionality with corpus data."""
        result = mots_de_n_lettres(corpus_set, 15)
        assert isinstance(result, set)
        # Based on the doctest in main.py, we expect 8730 words of 15 letters
        assert len(result) == 8730
        
        # All words should have exactly 15 letters
        for word in result:
            assert len(word) == 15
    
    def test_mots_de_n_lettres_corpus_specific_lengths(self, corpus_set):
        """Test specific length counts from corpus based on doctest examples."""
        
        expected_counts = {
            15: 8730, 16: 4418, 17: 2120, 18: 977, 19: 437, 
            20: 205, 21: 94, 22: 42, 23: 11, 24: 4, 25: 2
        }
        
        for length, expected_count in expected_counts.items():
            result = mots_de_n_lettres(corpus_set, length)
            assert len(result) == expected_count, f"Expected {expected_count} words of {length} letters, got {len(result)}"
    
    def test_mots_de_n_lettres_corpus_specific_words(self, corpus_set):
        """Test specific words from corpus based on doctest examples."""
        # Test 23-letter words
        result_23 = mots_de_n_lettres(corpus_set, 23)
        sorted_23 = sorted(list(result_23))
        assert sorted_23[0] == 'constitutionnalisassent'
        
        # Test 24-letter words
        result_24 = mots_de_n_lettres(corpus_set, 24)
        sorted_24 = sorted(list(result_24))
        expected_24 = ['constitutionnalisassions', 'constitutionnaliseraient', 
                      'hospitalo-universitaires', 'oto-rhino-laryngologiste']
        assert sorted_24 == expected_24
        
        # Test 25-letter words
        result_25 = mots_de_n_lettres(corpus_set, 25)
        sorted_25 = sorted(list(result_25))
        expected_25 = ['anticonstitutionnellement', 'oto-rhino-laryngologistes']
        assert sorted_25 == expected_25
    
    def test_mots_de_n_lettres_empty_set(self):
        """Test with empty set."""
        empty_set = set()
        result = mots_de_n_lettres(empty_set, 5)
        assert result == set()
        assert isinstance(result, set)
    
    def test_mots_de_n_lettres_no_words_of_length(self, corpus_set):
        """Test with length that doesn't exist in corpus."""
        # Test with very large length that shouldn't exist
        result = mots_de_n_lettres(corpus_set, 50)
        assert result == set()
        assert isinstance(result, set)
        
        # Test with length 0
        result_zero = mots_de_n_lettres(corpus_set, 0)
        assert result_zero == set()
    
    def test_mots_de_n_lettres_single_letter_words(self, corpus_set):
        """Test with single letter words."""
        result = mots_de_n_lettres(corpus_set, 1)
        assert isinstance(result, set)
        # Should contain at least 'a' and 'à'
        assert 'a' in result
        assert 'à' in result
        
        # All words should have exactly 1 letter
        for word in result:
            assert len(word) == 1
    
    def test_mots_de_n_lettres_two_letter_words(self, corpus_set):
        """Test with two letter words."""
        result = mots_de_n_lettres(corpus_set, 2)
        assert isinstance(result, set)
        
        # Should contain common 2-letter French words
        common_2_letter = {'le', 'la', 'de', 'et', 'en', 'un', 'il', 'je', 'tu', 'on', 'ce', 'se', 'ne', 'me', 'te', 'du'}
        for word in common_2_letter:
            if word in corpus_set:  # Only test if it exists in corpus
                assert word in result
        
        # All words should have exactly 2 letters
        for word in result:
            assert len(word) == 2
    
    def test_mots_de_n_lettres_common_lengths(self, corpus_set):
        """Test with common word lengths."""
        # Test common word lengths and verify they return reasonable numbers
        for length in [3, 4, 5, 6, 7, 8, 9, 10]:
            result = mots_de_n_lettres(corpus_set, length)
            assert isinstance(result, set)
            assert len(result) > 0, f"No words of length {length} found"
            
            # All words should have exactly the specified length
            for word in result:
                assert len(word) == length
    
    def test_mots_de_n_lettres_negative_length(self, corpus_set):
        """Test with negative length."""
        result = mots_de_n_lettres(corpus_set, -1)
        assert result == set()
        assert isinstance(result, set)
    
    
    def test_mots_de_n_lettres_with_accented_words(self):
        """Test mots_de_n_lettres with French accented words."""
        test_words = {'café', 'être', 'français', 'déjà', 'très', 'où', 'à'}
        
        # Test length 1
        result_1 = mots_de_n_lettres(test_words, 1)
        assert result_1 == {'à'}
        
        # Test length 2
        result_2 = mots_de_n_lettres(test_words, 2)
        assert result_2 == {'où'}
        
        # Test length 4
        result_4 = mots_de_n_lettres(test_words, 4)
        assert result_4 == {'café', 'être', 'déjà', 'très'}
        
        # Test length 8
        result_8 = mots_de_n_lettres(test_words, 8)
        assert result_8 == {'français'}
    
    def test_mots_de_n_lettres_preserves_set_type(self, corpus_set):
        """Test that the function always returns a set."""
        for length in [1, 5, 10, 15, 100]:
            result = mots_de_n_lettres(corpus_set, length)
            assert isinstance(result, set)
    
    def test_mots_de_n_lettres_subset_property(self, corpus_set):
        """Test that result is always a subset of the input."""
        for length in [1, 5, 10, 15]:
            result = mots_de_n_lettres(corpus_set, length)
            assert result.issubset(corpus_set)
    
    def test_mots_de_n_lettres_no_modification_of_input(self, corpus_set):
        """Test that the input set is not modified."""
        original_length = len(corpus_set)
        original_copy = corpus_set.copy()
        
        # Call function multiple times
        mots_de_n_lettres(corpus_set, 5)
        mots_de_n_lettres(corpus_set, 10)
        mots_de_n_lettres(corpus_set, 15)
        
        # Check that original set is unchanged
        assert len(corpus_set) == original_length
        assert corpus_set == original_copy
    
    def test_mots_de_n_lettres_with_special_characters(self, corpus_set):
        """Test with words containing special characters from corpus.txt."""
        
        # Test length 5 - short hyphenated words
        result_5 = mots_de_n_lettres(corpus_set, 5)
        expected_5_words = {'à-pic', 'ai-je', 'as-tu', 'es-tu', 'hi-fi'}
        # Check that these words are in the result (they should be in corpus)
        for word in expected_5_words:
            if word in corpus_set:  # Only test if word exists in corpus
                assert word in result_5, f"Expected '{word}' in 5-letter words"
        
        # Test length 6 - medium hyphenated words
        result_6 = mots_de_n_lettres(corpus_set, 6)
        expected_6_words = {'a-t-il', 'est-ce', 'hi-han', 'pin-up'}
        for word in expected_6_words:
            if word in corpus_set:
                assert word in result_6, f"Expected '{word}' in 6-letter words"
        
        # Test length 14 - abaisse-langue from corpus
        result_14 = mots_de_n_lettres(corpus_set, 14)
        if 'abaisse-langue' in corpus_set:
            assert 'abaisse-langue' in result_14
        
        # Test length 23 - hospitalo-universitaire  
        result_23 = mots_de_n_lettres(corpus_set, 23)
        if 'hospitalo-universitaire' in corpus_set:
            assert 'hospitalo-universitaire' in result_23
        
        # Test length 24 - hospitalo-universitaires
        result_24 = mots_de_n_lettres(corpus_set, 24)
        if 'hospitalo-universitaires' in corpus_set:
            assert 'hospitalo-universitaires' in result_24
        
        # Test length 25 - oto-rhino-laryngologistes (longest hyphenated word)
        result_25 = mots_de_n_lettres(corpus_set, 25)
        if 'oto-rhino-laryngologistes' in corpus_set:
            assert 'oto-rhino-laryngologistes' in result_25
        
        # Verify all results are sets and contain only words of correct length
        for length, result in [(5, result_5), (6, result_6), (14, result_14), 
                              (23, result_23), (24, result_24), (25, result_25)]:
            assert isinstance(result, set)
            for word in result:
                assert len(word) == length, f"Word '{word}' has length {len(word)}, expected {length}"
    
    
    @pytest.mark.skipif(not os.path.exists(FILENAME), reason="Corpus file not available")
    def test_mots_de_n_lettres_conditional_skip(self, corpus_set):
        """Example test that will be skipped if corpus file is not available."""
        result = mots_de_n_lettres(corpus_set, 5)
        assert isinstance(result, set)


class TestMotsAvec:
    """Test class for the mots_avec function."""
    
    def test_mots_avec_corpus_basic_k(self, corpus_set):
        """Test basic functionality with 'k' from corpus data (from doctest)."""
        result = mots_avec(corpus_set, 'k')
        assert isinstance(result, set)
        # Based on the doctest in main.py, we expect 1621 words with 'k'
        assert len(result) == 1621
        
        # All words should contain 'k'
        for word in result:
            assert 'k' in word, f"Word '{word}' should contain 'k'"
    
    def test_mots_avec_corpus_specific_k_words(self, corpus_set):
        """Test specific k words from corpus based on doctest examples."""
        mk = mots_avec(corpus_set, 'k')
        sorted_mk = sorted(list(mk))
        
        # Test specific indices from the doctest
        expected_words_35_74_7 = ['ankyloseraient', 'ankyloserons', 'ankylostome', 'ankylosée', 'ashkénaze', 'bachi-bouzouks']
        actual_words_35_74_7 = sorted_mk[35:74:7]
        assert actual_words_35_74_7 == expected_words_35_74_7
        
        expected_words_147_359_38 = ['black', 'blackboulèrent', 'cheikhs', 'cokéfierais', 'dock', 'dénickeliez']
        actual_words_147_359_38 = sorted_mk[147:359:38]
        assert actual_words_147_359_38 == expected_words_147_359_38
        
        expected_words_999_122 = ['képi', 'nickela', 'parkérisiez', 'semi-coke', 'stockais', 'week-end']
        actual_words_999_122 = sorted_mk[999::122]
        assert actual_words_999_122 == expected_words_999_122
    
    def test_mots_avec_common_letters(self, corpus_set):
        """Test with common French letters."""
        # Test with 'e' - should be very common
        result_e = mots_avec(corpus_set, 'e')
        assert isinstance(result_e, set)
        assert len(result_e) > 50000  # 'e' is very common in French
        
        # Test with 'r' - also common
        result_r = mots_avec(corpus_set, 'r')
        assert isinstance(result_r, set)
        assert len(result_r) > 20000
        
        # Test with 'a' - very common
        result_a = mots_avec(corpus_set, 'a')
        assert isinstance(result_a, set)
        assert len(result_a) > 30000
    
    def test_mots_avec_rare_letters(self, corpus_set):
        """Test with rare letters."""
        # Test with 'w' - rare in French
        result_w = mots_avec(corpus_set, 'w')
        assert isinstance(result_w, set)
        assert len(result_w) < 1000  # 'w' is rare in French
        
        # Test with 'x' - also rare
        result_x = mots_avec(corpus_set, 'x')
        assert isinstance(result_x, set)
        assert len(result_x) < 9000
        
        # Test with 'z' - rare but more common than w
        result_z = mots_avec(corpus_set, 'z')
        assert isinstance(result_z, set)
        assert len(result_z) > 1000  # More common than w
    
    def test_mots_avec_accented_characters(self, corpus_set):
        """Test with French accented characters."""
        # Test with 'é'
        result_e_acute = mots_avec(corpus_set, 'é')
        assert isinstance(result_e_acute, set)
        assert len(result_e_acute) > 1000
        
        # Test with 'à'
        result_a_grave = mots_avec(corpus_set, 'à')
        assert isinstance(result_a_grave, set)
        assert len(result_a_grave) > 40
        
        # Test with 'ç'
        result_c_cedilla = mots_avec(corpus_set, 'ç')
        assert isinstance(result_c_cedilla, set)
        assert len(result_c_cedilla) > 50
    
    def test_mots_avec_multi_character_strings(self, corpus_set):
        """Test with multi-character substrings."""
        # Test with 'tion' - common French ending
        result_tion = mots_avec(corpus_set, 'tion')
        assert isinstance(result_tion, set)
        assert len(result_tion) > 5000
        
        # Test with 'ment' - common French ending
        result_ment = mots_avec(corpus_set, 'ment')
        assert isinstance(result_ment, set)
        assert len(result_ment) > 3000
        
        # Test with 'anti' - common French prefix
        result_anti = mots_avec(corpus_set, 'anti')
        assert isinstance(result_anti, set)
        assert len(result_anti) > 100
        
        # Test with 'pre' - common prefix
        result_pre = mots_avec(corpus_set, 'pre')
        assert isinstance(result_pre, set)
        assert len(result_pre) > 1000
    
    def test_mots_avec_special_characters(self, corpus_set):
        """Test with special characters found in French words."""
        # Test with hyphen
        result_hyphen = mots_avec(corpus_set, '-')
        assert isinstance(result_hyphen, set)
        assert len(result_hyphen) > 100  # Many compound words have hyphens
        
        # Test with apostrophe (if any exist)
        result_apostrophe = mots_avec(corpus_set, "'")
        assert isinstance(result_apostrophe, set)
        # May be 0 if no words with apostrophes in corpus
    
    def test_mots_avec_vowel_combinations(self, corpus_set):
        """Test with vowel combinations."""
        # Test with 'ou' - common in French
        result_ou = mots_avec(corpus_set, 'ou')
        assert isinstance(result_ou, set)
        assert len(result_ou) > 5000
        
        # Test with 'eau' - common French pattern
        result_eau = mots_avec(corpus_set, 'eau')
        assert isinstance(result_eau, set)
        assert len(result_eau) > 900
        
        # Test with 'ai' - common French diphthong
        result_ai = mots_avec(corpus_set, 'ai')
        assert isinstance(result_ai, set)
        assert len(result_ai) > 3000
    
    def test_mots_avec_consonant_clusters(self, corpus_set):
        """Test with consonant clusters."""
        # Test with 'ch' - common in French
        result_ch = mots_avec(corpus_set, 'ch')
        assert isinstance(result_ch, set)
        assert len(result_ch) > 2000
        
        # Test with 'qu' - very common in French
        result_qu = mots_avec(corpus_set, 'qu')
        assert isinstance(result_qu, set)
        assert len(result_qu) > 3000
        
        # Test with 'ph' - less common but present
        result_ph = mots_avec(corpus_set, 'ph')
        assert isinstance(result_ph, set)
        assert len(result_ph) > 500
    
    def test_mots_avec_empty_string(self, corpus_set):
        """Test with empty string - should return all words."""
        result = mots_avec(corpus_set, '')
        assert isinstance(result, set)
        assert result == corpus_set  # Empty string is in every word
        assert len(result) == len(corpus_set)
    
    def test_mots_avec_empty_set(self):
        """Test with empty set."""
        empty_set = set()
        result = mots_avec(empty_set, 'a')
        assert result == set()
        assert isinstance(result, set)
    
    def test_mots_avec_nonexistent_substring(self, corpus_set):
        """Test with substring that doesn't exist in any word."""
        # Use a combination that's unlikely to exist
        result = mots_avec(corpus_set, 'xyz123')
        assert isinstance(result, set)
        assert len(result) == 0
        
        # Test with another unlikely combination
        result2 = mots_avec(corpus_set, 'qwxz')
        assert isinstance(result2, set)
        assert len(result2) == 0
    
    def test_mots_avec_case_sensitivity(self, corpus_set):
        """Test case sensitivity."""
        # Test lowercase vs uppercase (assuming corpus is lowercase)
        result_lower = mots_avec(corpus_set, 'a')
        result_upper = mots_avec(corpus_set, 'A')
        
        # If corpus is all lowercase, uppercase should return empty set
        if len(result_upper) == 0:
            assert len(result_lower) > len(result_upper)
    
    def test_mots_avec_with_mock_data(self):
        """Test mots_avec with controlled mock data."""
        test_words = {'hello', 'world', 'python', 'test', 'help', 'programming'}
        
        # Test with 'o'
        result_o = mots_avec(test_words, 'o')
        expected_o = {'hello', 'world', 'python', 'programming'}
        assert result_o == expected_o
        
        # Test with 'p'
        result_p = mots_avec(test_words, 'p')
        expected_p = {'python', 'help', 'programming'}
        assert result_p == expected_p
        
        # Test with 'gram'
        result_gram = mots_avec(test_words, 'gram')
        expected_gram = {'programming'}
        assert result_gram == expected_gram
        
        # Test with 'xyz' (not in any word)
        result_xyz = mots_avec(test_words, 'xyz')
        assert result_xyz == set()
    
    def test_mots_avec_subset_property(self, corpus_set):
        """Test that result is always a subset of the input."""
        for substring in ['a', 'tion', 'k', 'xyz']:
            result = mots_avec(corpus_set, substring)
            assert result.issubset(corpus_set)
    
    def test_mots_avec_preserves_set_type(self, corpus_set):
        """Test that the function always returns a set."""
        for substring in ['a', 'e', 'tion', 'k', '']:
            result = mots_avec(corpus_set, substring)
            assert isinstance(result, set)
    
    def test_mots_avec_no_modification_of_input(self, corpus_set):
        """Test that the input set is not modified."""
        original_length = len(corpus_set)
        original_copy = corpus_set.copy()
        
        # Call function multiple times
        mots_avec(corpus_set, 'a')
        mots_avec(corpus_set, 'tion')
        mots_avec(corpus_set, 'k')
        
        # Check that original set is unchanged
        assert len(corpus_set) == original_length
        assert corpus_set == original_copy
    
    def test_mots_avec_intersection_patterns(self, corpus_set):
        """Test intersection of different character patterns."""
        # Words with both 'k' and 'w' (should be rare)
        mk = mots_avec(corpus_set, 'k')
        mw = mots_avec(corpus_set, 'w')
        mkw = mk & mw
        assert isinstance(mkw, set)
        assert len(mkw) < len(mk)  # Should be smaller than just 'k' words
        assert len(mkw) < len(mw)  # Should be smaller than just 'w' words
        
        # Words with both 'qu' and 'tion'
        mqu = mots_avec(corpus_set, 'qu')
        mtion = mots_avec(corpus_set, 'tion')
        mqu_tion = mqu & mtion
        assert isinstance(mqu_tion, set)
        # Should contain words like "question", "liquidation", etc.
        assert len(mqu_tion) > 0
    
    def test_mots_avec_with_numbers_in_words(self, corpus_set):
        """Test with numbers (if any exist in corpus)."""
        result_1 = mots_avec(corpus_set, '1')
        result_2 = mots_avec(corpus_set, '2')
        
        # Numbers are unlikely in a French word corpus
        assert isinstance(result_1, set)
        assert isinstance(result_2, set)
        # Most likely empty, but we don't assert that in case there are technical terms


class TestCherche1:
    """Test class for the cherche1 function."""
    
    def test_cherche1_corpus_basic_z_z_7(self, corpus_set):
        """Test basic functionality with 'z','z',7 from corpus data (from doctest)."""
        result = cherche1(corpus_set, 'z', 'z', 7)
        assert isinstance(result, set)
        # Based on the doctest in main.py, we expect 10 words
        assert len(result) == 10
        
        # All words should start with 'z', end with 'z', and have exactly 7 letters
        for word in result:
            assert word.startswith('z'), f"Word '{word}' should start with 'z'"
            assert word.endswith('z'), f"Word '{word}' should end with 'z'"
            assert len(word) == 7, f"Word '{word}' should have 7 letters, has {len(word)}"
    
    def test_cherche1_corpus_specific_z_words(self, corpus_set):
        """Test specific z words from corpus based on doctest examples."""
        result = cherche1(corpus_set, 'z', 'z', 7)
        sorted_result = sorted(list(result))
        
        # Test specific slice from the doctest
        expected_words = ['zinguez', 'zippiez', 'zonerez']
        actual_words = sorted_result[4:7]
        assert actual_words == expected_words
    
    def test_cherche1_single_letter_words(self, corpus_set):
        """Test with single letter words."""
        # Test 'a' to 'a' with length 1
        result_a = cherche1(corpus_set, 'a', 'a', 1)
        assert isinstance(result_a, set)
        assert len(result_a) == 1
        assert 'a' in result_a
        
        # Test 'à' to 'à' with length 1
        result_a_accent = cherche1(corpus_set, 'à', 'à', 1)
        assert isinstance(result_a_accent, set)
        assert len(result_a_accent) == 1
        assert 'à' in result_a_accent
    
    def test_cherche1_common_patterns(self, corpus_set):
        """Test common French word patterns."""
        # Test words starting with 'a' and ending with 'e' of length 4
        result_a_e_4 = cherche1(corpus_set, 'a', 'e', 4)
        assert isinstance(result_a_e_4, set)
        assert len(result_a_e_4) == 23
        
        # Should contain common words like 'aide', 'aime', etc.
        common_words = {'aide', 'aime', 'aire', 'aise'}
        for word in common_words:
            if word in corpus_set:
                assert word in result_a_e_4, f"Expected '{word}' in a-e-4 results"
        
        # All words should match the pattern
        for word in result_a_e_4:
            assert word.startswith('a')
            assert word.endswith('e')
            assert len(word) == 4
    
    def test_cherche1_verb_patterns(self, corpus_set):
        """Test French verb patterns."""
        # Test 're-' prefix verbs ending in 'er' (infinitives)
        result_re_er_8 = cherche1(corpus_set, 're', 'er', 8)
        assert isinstance(result_re_er_8, set)
        assert len(result_re_er_8) == 92
        
        # Should contain words like 'rebander', 'rebeller', etc.
        expected_words = {'rebander', 'rebeller', 'rebiffer'}
        for word in expected_words:
            if word in corpus_set:
                assert word in result_re_er_8, f"Expected '{word}' in re-er-8 results"
    
    def test_cherche1_plural_patterns(self, corpus_set):
        """Test plural word patterns."""
        # Test words starting with 'un' and ending with 's' (some plurals/conjugations)
        result_un_s_6 = cherche1(corpus_set, 'un', 's', 6)
        assert isinstance(result_un_s_6, set)
        assert len(result_un_s_6) == 6
        
        # Should contain words like 'unions', 'uniras', etc.
        expected_words = {'unions', 'uniras', 'unités'}
        for word in expected_words:
            if word in corpus_set:
                assert word in result_un_s_6, f"Expected '{word}' in un-s-6 results"
    
    def test_cherche1_empty_start(self, corpus_set):
        """Test with empty start string."""
        # Words ending with 'e' of length 3 (any start)
        result = cherche1(corpus_set, '', 'e', 3)
        assert isinstance(result, set)
        assert len(result) == 51
        
        # All words should end with 'e' and have length 3
        for word in result:
            assert word.endswith('e')
            assert len(word) == 3
        
        # Should contain words like 'une', 'rue', 'vue', etc.
        common_words = {'une', 'rue', 'vue', 'due'}
        for word in common_words:
            if word in corpus_set:
                assert word in result, f"Expected '{word}' in empty-e-3 results"
    
    def test_cherche1_empty_stop(self, corpus_set):
        """Test with empty stop string."""
        # Words starting with 'a' of length 3 (any ending)
        result = cherche1(corpus_set, 'a', '', 3)
        assert isinstance(result, set)
        assert len(result) == 22
        
        # All words should start with 'a' and have length 3
        for word in result:
            assert word.startswith('a')
            assert len(word) == 3
        
        # Should contain words like 'ami', 'art', 'ans', etc.
        common_words = {'ami', 'art', 'ans', 'aux'}
        for word in common_words:
            if word in corpus_set:
                assert word in result, f"Expected '{word}' in a-empty-3 results"
    
    def test_cherche1_empty_start_and_stop(self, corpus_set):
        """Test with empty start and stop strings."""
        # All words of length 3
        result = cherche1(corpus_set, '', '', 3)
        assert isinstance(result, set)
        assert len(result) == 469
        
        # All words should have length 3
        for word in result:
            assert len(word) == 3
        
        # Should be equivalent to mots_de_n_lettres(corpus_set, 3)
        expected = mots_de_n_lettres(corpus_set, 3)
        assert result == expected
    
    def test_cherche1_longer_prefixes_suffixes(self, corpus_set):
        """Test with longer prefix and suffix patterns."""
        # Test 'anti-' prefix with '-tion' suffix
        result_anti_tion = cherche1(corpus_set, 'anti', 'tion', 12)
        assert isinstance(result_anti_tion, set)
        
        # Test 'pre-' prefix with '-ment' suffix
        result_pre_ment = cherche1(corpus_set, 'pre', 'ment', 10)
        assert isinstance(result_pre_ment, set)
        
        # All results should match the patterns
        for word in result_anti_tion:
            assert word.startswith('anti')
            assert word.endswith('tion')
            assert len(word) == 12
        
        for word in result_pre_ment:
            assert word.startswith('pre')
            assert word.endswith('ment')
            assert len(word) == 10
    
    def test_cherche1_accented_patterns(self, corpus_set):
        """Test with accented characters."""
        # Test words starting with 'é' and ending with 'e'
        result_e_accent = cherche1(corpus_set, 'é', 'e', 5)
        assert isinstance(result_e_accent, set)
        
        # Test words starting with 'à' 
        result_a_grave = cherche1(corpus_set, 'à', 'e', 6)
        assert isinstance(result_a_grave, set)
        
        # All results should match the patterns
        for word in result_e_accent:
            assert word.startswith('é')
            assert word.endswith('e')
            assert len(word) == 5
    
    def test_cherche1_no_matches(self, corpus_set):
        """Test patterns that should return no matches."""
        # Impossible combination: start with 'z', end with 'z', but length 1000
        result = cherche1(corpus_set, 'z', 'z', 1000)
        assert isinstance(result, set)
        assert len(result) == 0
        
        # Start with 'xyz' (unlikely to exist)
        result2 = cherche1(corpus_set, 'xyz', 'e', 5)
        assert isinstance(result2, set)
        assert len(result2) == 0
        
        # End with 'xyz' (unlikely to exist)
        result3 = cherche1(corpus_set, 'a', 'xyz', 5)
        assert isinstance(result3, set)
        assert len(result3) == 0
    
    def test_cherche1_edge_cases_length(self, corpus_set):
        """Test edge cases with different lengths."""
        # Length 0
        result_0 = cherche1(corpus_set, 'a', 'a', 0)
        assert isinstance(result_0, set)
        assert len(result_0) == 0
        
        # Negative length
        result_neg = cherche1(corpus_set, 'a', 'a', -1)
        assert isinstance(result_neg, set)
        assert len(result_neg) == 0
        
        # Very long length
        result_long = cherche1(corpus_set, 'a', 'e', 50)
        assert isinstance(result_long, set)
        assert len(result_long) == 0
    
    def test_cherche1_case_sensitivity(self, corpus_set):
        """Test case sensitivity."""
        # Test lowercase vs uppercase (assuming corpus is lowercase)
        result_lower = cherche1(corpus_set, 'a', 'e', 4)
        result_upper_start = cherche1(corpus_set, 'A', 'e', 4)
        result_upper_end = cherche1(corpus_set, 'a', 'E', 4)
        
        assert isinstance(result_lower, set)
        assert isinstance(result_upper_start, set)
        assert isinstance(result_upper_end, set)
        
        # Uppercase versions should likely return fewer or no results
        assert len(result_upper_start) <= len(result_lower)
        assert len(result_upper_end) <= len(result_lower)
    
    def test_cherche1_with_mock_data(self):
        """Test cherche1 with controlled mock data."""
        test_words = {'hello', 'world', 'python', 'test', 'help', 'programming', 'app', 'web'}
        
        # Test 'h' to 'o' with length 5
        result1 = cherche1(test_words, 'h', 'o', 5)
        expected1 = {'hello'}
        assert result1 == expected1
        
        # Test 'p' to 'n' with length 6
        result2 = cherche1(test_words, 'p', 'n', 6)
        expected2 = {'python'}
        assert result2 == expected2
        
        # Test '' to 'p' with length 3
        result3 = cherche1(test_words, '', 'p', 3)
        expected3 = {'app'}
        assert result3 == expected3
        
        # Test 'w' to '' with length 5
        result4 = cherche1(test_words, 'w', '', 5)
        expected4 = {'world'}
        assert result4 == expected4
        
        # Test no matches
        result5 = cherche1(test_words, 'x', 'y', 5)
        assert result5 == set()
    
    def test_cherche1_subset_property(self, corpus_set):
        """Test that result is always a subset of the input."""
        test_cases = [
            ('a', 'e', 4),
            ('z', 'z', 7),
            ('re', 'er', 8),
            ('', 'e', 3),
            ('a', '', 3)
        ]
        
        for start, stop, n in test_cases:
            result = cherche1(corpus_set, start, stop, n)
            assert result.issubset(corpus_set)
    
    def test_cherche1_preserves_set_type(self, corpus_set):
        """Test that the function always returns a set."""
        test_cases = [
            ('a', 'e', 4),
            ('z', 'z', 7),
            ('xyz', 'abc', 5),
            ('', '', 3)
        ]
        
        for start, stop, n in test_cases:
            result = cherche1(corpus_set, start, stop, n)
            assert isinstance(result, set)
    
    def test_cherche1_no_modification_of_input(self, corpus_set):
        """Test that the input set is not modified."""
        original_length = len(corpus_set)
        original_copy = corpus_set.copy()
        
        # Call function multiple times
        cherche1(corpus_set, 'a', 'e', 4)
        cherche1(corpus_set, 'z', 'z', 7)
        cherche1(corpus_set, 're', 'er', 8)
        
        # Check that original set is unchanged
        assert len(corpus_set) == original_length
        assert corpus_set == original_copy
    
    def test_cherche1_empty_set_input(self):
        """Test with empty set input."""
        empty_set = set()
        result = cherche1(empty_set, 'a', 'e', 4)
        assert result == set()
        assert isinstance(result, set)
    
    def test_cherche1_relationship_with_other_functions(self, corpus_set):
        """Test relationship with mots_de_n_lettres and mots_avec."""
        # cherche1 with empty start and stop should equal mots_de_n_lettres
        result1 = cherche1(corpus_set, '', '', 5)
        result2 = mots_de_n_lettres(corpus_set, 5)
        assert result1 == result2
        
        # cherche1 result should be subset of mots_de_n_lettres result
        result3 = cherche1(corpus_set, 'a', 'e', 6)
        result4 = mots_de_n_lettres(corpus_set, 6)
        assert result3.issubset(result4)
        
        # cherche1 result should be subset of mots_avec results
        if len(result3) > 0:  # Only test if there are results
            result5 = mots_avec(corpus_set, 'a')  # Words containing 'a'
            result6 = mots_avec(corpus_set, 'e')  # Words containing 'e'
            # All words starting with 'a' should contain 'a'
            assert result3.issubset(result5)
            # All words ending with 'e' should contain 'e'
            assert result3.issubset(result6)


class TestCherche2:
    """Test class for the cherche2 function."""
    
    def test_cherche2_corpus_basic_doctest(self, corpus_set):
        """Test basic functionality with doctest example."""
        result = cherche2(corpus_set, ['a'], ['b'], ['z'], 16, 16)
        assert isinstance(result, set)
        # Based on the doctest in main.py, we expect 1 word
        assert len(result) == 1
        assert result == {'alphabétisassiez'}
        
        # Verify the word meets all criteria
        word = list(result)[0]
        assert word.startswith('a')
        assert 'b' in word
        assert word.endswith('z')
        assert len(word) == 16
    
    def test_cherche2_multiple_start_options(self, corpus_set):
        """Test with multiple start options."""
        result = cherche2(corpus_set, ['a', 'e'], ['i'], ['e', 's'], 5, 8)
        assert isinstance(result, set)
        assert len(result) == 2095
        
        # All words should start with 'a' or 'e', contain 'i', end with 'e' or 's', length 5-8
        for word in list(result)[:100]:  # Test sample for performance
            assert word.startswith('a') or word.startswith('e')
            assert 'i' in word
            assert word.endswith('e') or word.endswith('s')
            assert 5 <= len(word) <= 8
    
    def test_cherche2_verb_patterns(self, corpus_set):
        """Test French verb patterns."""
        # Test re-tion-er pattern (repositionner)
        result1 = cherche2(corpus_set, ['re'], ['tion'], ['er'], 10, 15)
        assert isinstance(result1, set)
        assert len(result1) == 1
        assert 'repositionner' in result1
        
        # Test pre/de prefixes with 'i' and 'er' ending
        result2 = cherche2(corpus_set, ['pre', 'de'], ['i'], ['er'], 8, 12)
        assert isinstance(result2, set)
        assert len(result2) == 10
        
        # Should contain words like 'dessiner', 'destiner', etc.
        expected_words = {'dessiner', 'destiner', 'destituer'}
        for word in expected_words:
            if word in corpus_set:
                assert word in result2
    
    def test_cherche2_common_french_patterns(self, corpus_set):
        """Test common French word patterns."""
        # Test 'a' start, 'r' middle, 'e' end pattern
        result1 = cherche2(corpus_set, ['a'], ['r'], ['e'], 5, 8)
        assert isinstance(result1, set)
        assert len(result1) == 466
        
        # Should contain words like 'abordage', 'abordee', etc.
        sample_words = {'abordage', 'aborde', 'abordée'}
        for word in sample_words:
            if word in corpus_set:
                assert word in result1
        
        # Test 'con' prefix with 'tion' and 'e' ending
        result2 = cherche2(corpus_set, ['con'], ['tion'], ['e'], 10, 15)
        assert isinstance(result2, set)
        assert len(result2) == 16
        
        # Should contain conditional forms
        expected_words = {'conditionne', 'conditionnée'}
        for word in expected_words:
            if word in corpus_set:
                assert word in result2
    
    def test_cherche2_technical_terms(self, corpus_set):
        """Test with technical/scientific terms."""
        # Test 'auto' with 'mat' and 'ment' - should find 'automatiquement'
        result = cherche2(corpus_set, ['auto'], ['mat'], ['ment'], 12, 18)
        assert isinstance(result, set)
        assert len(result) == 1
        assert 'automatiquement' in result
    
    def test_cherche2_length_ranges(self, corpus_set):
        """Test different length ranges."""
        # Short words (3-5 letters)
        result1 = cherche2(corpus_set, ['a'], ['i'], ['e'], 3, 5)
        assert isinstance(result1, set)
        
        # Medium words (6-10 letters)
        result2 = cherche2(corpus_set, ['a'], ['i'], ['e'], 6, 10)
        assert isinstance(result2, set)
        
        # Long words (15-20 letters)
        result3 = cherche2(corpus_set, ['a'], ['i'], ['e'], 15, 20)
        assert isinstance(result3, set)
        
        # Verify length constraints
        for word in list(result1)[:50]:  # Sample for performance
            assert 3 <= len(word) <= 5
        
        for word in list(result2)[:50]:
            assert 6 <= len(word) <= 10
        
        for word in list(result3):  # All words since likely few
            assert 15 <= len(word) <= 20
    
    def test_cherche2_single_length(self, corpus_set):
        """Test with single length (nmin == nmax)."""
        # Test exact length of 7
        result = cherche2(corpus_set, ['m'], ['a'], ['e'], 7, 7)
        assert isinstance(result, set)
        
        # All words should have exactly 7 letters
        for word in result:
            assert len(word) == 7
            assert word.startswith('m')
            assert 'a' in word
            assert word.endswith('e')
    
    def test_cherche2_empty_lists_behavior(self, corpus_set):
        """Test behavior with empty lists."""
        # According to the implementation, empty lists result in empty intersections
        
        # Empty start list
        result1 = cherche2(corpus_set, [], ['a'], ['e'], 5, 7)
        assert isinstance(result1, set)
        assert len(result1) == 0  # Empty start means no words match
        
        # Empty middle list  
        result2 = cherche2(corpus_set, ['a'], [], ['e'], 5, 7)
        assert isinstance(result2, set)
        assert len(result2) == 0  # Empty middle means no words match
        
        # Empty end list
        result3 = cherche2(corpus_set, ['a'], ['i'], [], 5, 7)
        assert isinstance(result3, set)
        assert len(result3) == 0  # Empty end means no words match
        
        # All empty lists
        result4 = cherche2(corpus_set, [], [], [], 5, 7)
        assert isinstance(result4, set)
        assert len(result4) == 0
    
    def test_cherche2_no_matches(self, corpus_set):
        """Test patterns that should return no matches."""
        # Impossible combination
        result1 = cherche2(corpus_set, ['xyz'], ['abc'], ['uvw'], 5, 10)
        assert isinstance(result1, set)
        assert len(result1) == 0
        
        # Length range with no words
        result2 = cherche2(corpus_set, ['a'], ['e'], ['s'], 100, 200)
        assert isinstance(result2, set)
        assert len(result2) == 0
        
        # Contradictory patterns (start with 'z', end with 'a', but very short)
        result3 = cherche2(corpus_set, ['z'], ['x'], ['a'], 1, 2)
        assert isinstance(result3, set)
        assert len(result3) == 0
    
    def test_cherche2_accented_characters(self, corpus_set):
        """Test with French accented characters."""
        # Test words with 'é'
        result1 = cherche2(corpus_set, ['é'], ['e'], ['e'], 5, 10)
        assert isinstance(result1, set)
        
        # Test words starting with 'à'
        result2 = cherche2(corpus_set, ['à'], ['o'], ['s'], 4, 8)
        assert isinstance(result2, set)
        
        # Verify accented characters are handled correctly
        for word in result1:
            assert word.startswith('é')
            assert 'e' in word
            assert word.endswith('e')
    
    def test_cherche2_hyphenated_words(self, corpus_set):
        """Test with hyphenated words."""
        # Test compound words with hyphens
        result = cherche2(corpus_set, ['auto'], ['-'], ['e'], 10, 20)
        assert isinstance(result, set)
        
        # All results should contain hyphens
        for word in result:
            assert word.startswith('auto')
            assert '-' in word
            assert word.endswith('e')
    
    def test_cherche2_case_sensitivity(self, corpus_set):
        """Test case sensitivity."""
        # Test lowercase vs uppercase (assuming corpus is lowercase)
        result_lower = cherche2(corpus_set, ['a'], ['e'], ['s'], 5, 8)
        result_upper = cherche2(corpus_set, ['A'], ['E'], ['S'], 5, 8)
        
        assert isinstance(result_lower, set)
        assert isinstance(result_upper, set)
        
        # Uppercase should likely return fewer results
        assert len(result_upper) <= len(result_lower)
    
    def test_cherche2_overlapping_patterns(self, corpus_set):
        """Test overlapping start/mid/stop patterns."""
        # Test where start and middle could overlap
        result1 = cherche2(corpus_set, ['ab'], ['ba'], ['e'], 6, 10)
        assert isinstance(result1, set)
        
        # Test where middle and end could overlap  
        result2 = cherche2(corpus_set, ['a'], ['er'], ['re'], 6, 10)
        assert isinstance(result2, set)
        
        # Words should still meet all criteria
        for word in result1:
            assert word.startswith('ab')
            assert 'ba' in word
            assert word.endswith('e')
    
    def test_cherche2_with_mock_data(self):
        """Test cherche2 with controlled mock data."""
        test_words = {
            'hello', 'world', 'python', 'programming', 'test', 'development',
            'algorithm', 'computer', 'software', 'application'
        }
        
        # Test 'p' start, 'o' middle, 'g' end
        result1 = cherche2(test_words, ['p'], ['o'], ['g'], 8, 12)
        expected1 = {'programming'}
        assert result1 == expected1
        
        # Test multiple start options
        result2 = cherche2(test_words, ['a', 'c'], ['o'], ['r'], 6, 10)
        expected2 = {'computer'}
        assert result2 == expected2
        
        # Test no matches
        result3 = cherche2(test_words, ['x'], ['y'], ['z'], 5, 10)
        assert result3 == set()
        
        # Test with length constraints
        result4 = cherche2(test_words, [''], ['e'], [''], 4, 6)  # Any word 4-6 letters with 'e'
        expected4 = {'hello', 'test'}
        assert result4 == expected4
    
    def test_cherche2_edge_cases_length(self, corpus_set):
        """Test edge cases with length parameters."""
        # nmin > nmax (invalid range)
        result1 = cherche2(corpus_set, ['a'], ['e'], ['s'], 10, 5)
        assert isinstance(result1, set)
        assert len(result1) == 0  # No words can satisfy this
        
        # nmin = nmax = 0
        result2 = cherche2(corpus_set, ['a'], ['e'], ['s'], 0, 0)
        assert isinstance(result2, set)
        assert len(result2) == 0  # No words with length 0
        
        # Negative lengths
        result3 = cherche2(corpus_set, ['a'], ['e'], ['s'], -1, -1)
        assert isinstance(result3, set)
        assert len(result3) == 0
    
    def test_cherche2_subset_property(self, corpus_set):
        """Test that result is always a subset of the input."""
        test_cases = [
            (['a'], ['e'], ['s'], 5, 8),
            (['re'], ['tion'], ['er'], 10, 15),
            (['auto'], ['mat'], ['ment'], 12, 18),
            ([], ['a'], ['e'], 5, 7),
        ]
        
        for lstart, lmid, lstop, nmin, nmax in test_cases:
            result = cherche2(corpus_set, lstart, lmid, lstop, nmin, nmax)
            assert result.issubset(corpus_set)
    
    def test_cherche2_preserves_set_type(self, corpus_set):
        """Test that the function always returns a set."""
        test_cases = [
            (['a'], ['e'], ['s'], 5, 8),
            (['xyz'], ['abc'], ['uvw'], 5, 10),
            ([], [], [], 5, 7),
            (['a', 'e'], ['i', 'o'], ['s', 'e'], 3, 15)
        ]
        
        for lstart, lmid, lstop, nmin, nmax in test_cases:
            result = cherche2(corpus_set, lstart, lmid, lstop, nmin, nmax)
            assert isinstance(result, set)
    
    def test_cherche2_no_modification_of_input(self, corpus_set):
        """Test that the input set is not modified."""
        original_length = len(corpus_set)
        original_copy = corpus_set.copy()
        
        # Call function multiple times
        cherche2(corpus_set, ['a'], ['e'], ['s'], 5, 8)
        cherche2(corpus_set, ['re'], ['tion'], ['er'], 10, 15)
        cherche2(corpus_set, ['auto'], ['mat'], ['ment'], 12, 18)
        
        # Check that original set is unchanged
        assert len(corpus_set) == original_length
        assert corpus_set == original_copy
    
    def test_cherche2_empty_set_input(self):
        """Test with empty set input."""
        empty_set = set()
        result = cherche2(empty_set, ['a'], ['e'], ['s'], 5, 8)
        assert result == set()
        assert isinstance(result, set)
    
    def test_cherche2_relationship_with_other_functions(self, corpus_set):
        """Test relationship with other functions."""
        # cherche2 result should be subset of mots_de_n_lettres for the length range
        result1 = cherche2(corpus_set, ['a'], ['e'], ['s'], 6, 6)
        result2 = mots_de_n_lettres(corpus_set, 6)
        assert result1.issubset(result2)
        
        # cherche2 result should be subset of mots_avec for each pattern
        if len(result1) > 0:
            result3 = mots_avec(corpus_set, 'a')  # Words containing 'a'
            result4 = mots_avec(corpus_set, 'e')  # Words containing 'e'
            result5 = mots_avec(corpus_set, 's')  # Words containing 's'
            
            # All words should contain the required substrings
            assert result1.issubset(result3)  # All start with 'a' so contain 'a'
            assert result1.issubset(result4)  # All contain 'e'
            assert result1.issubset(result5)  # All end with 's' so contain 's'
        
        # Test relationship with cherche1
        result6 = cherche2(corpus_set, ['a'], ['e'], ['s'], 7, 7)
        result7 = cherche1(corpus_set, 'a', 's', 7)
        
        # cherche2 result should be subset of cherche1 result (more restrictive)
        assert result6.issubset(result7)
    
    def test_cherche2_performance_large_lists(self, corpus_set):
        """Test performance with larger option lists."""
        # Test with many start options
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
        
        result = cherche2(corpus_set, vowels, ['n'], consonants, 5, 8)
        assert isinstance(result, set)
        
        # All words should meet the criteria
        for word in list(result)[:100]:  # Sample for performance
            assert any(word.startswith(v) for v in vowels)
            assert 'n' in word
            assert any(word.endswith(c) for c in consonants)
            assert 5 <= len(word) <= 8


if __name__ == "__main__":
    # Allow running the tests directly
    pytest.main([__file__])


