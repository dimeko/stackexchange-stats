from stats.core import core
from stats.core import utils
import json

class TestUtils:
    def test_datetime_validation(self):
        assert utils.datetime_validation("invalid date") == False
        assert utils.datetime_validation("20220807 10:20:00") == True
        
    def test_normalize_date(self):
        assert utils.date_to_timestamp("20220807 10:00:00") == 1659855600
        assert utils.date_to_timestamp("20220807 10:20:00") == 1659856800
        
    def test_format_output(self):
        
        initial_json = {
            "total_answers": 39,
            "total_accepted_answers": 10,
            "top_answers_comments_count": {
                "73265744": 2,
                "73265746": 0,
                "73265762": 1,
            }
        }
            
        expected = {
            "json": json.dumps(initial_json, indent=2),
            "csv": ',0\ntotal_answers,39\ntotal_accepted_answers,10\ntop_answers_comments_count_73265744,2\ntop_answers_comments_count_73265746,0\ntop_answers_comments_count_73265762,1\n',
            "html": '<table border="1"><tr><th>total_answers</th><td>39</td></tr><tr><th>total_accepted_answers</th><td>10</td></tr><tr><th>top_answers_comments_count</th><td><table border="1"><tr><th>73265744</th><td>2</td></tr><tr><th>73265746</th><td>0</td></tr><tr><th>73265762</th><td>1</td></tr></table></td></tr></table>'
        }
        
        assert utils.format_output(initial_json, "json") == expected["json"]
        assert utils.format_output(initial_json, "csv") == expected["csv"]
        assert utils.format_output(initial_json, "html") == expected["html"]
        
class TestCore:
    def test_calculate_top_answers_comments(self):
        f = open('tests/test_data/score_answers_ids.json')
        data = json.load(f)
        output = {
            73247827: 2,
            73254735: 7,
            73253603: 3,
            73253930: 2,
            73247887: 0,
            73250470: 1,
            73250720: 4,
            73252220: 0,
            73250887: 0,
            73255281: 8
        }
        assert core.calculate_top_answers_comments(data) == output
        
    def test_stats(self, mocker):
        f = open('tests/test_data/success_api_response.json')
        mock_data = json.load(f)
        mocker.patch('stats.core.core.request', return_value=[mock_data["response"], "", 200])
        assert json.dumps(core.stats(1657177200, 1657177200, "", "", 200), sort_keys=True) == json.dumps(mock_data["result"], sort_keys=True)
