"""Unit tests for the emotion detection functions."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Validate that all emotion predictions return the correct dominant emotion."""

    def test_glad_sentence(self):
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_mad_sentence(self):
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_afraid_sentence(self):
        result = emotion_detector("I am so afraid that I cannot move")
        self.assertEqual(result["dominant_emotion"], "fear")

    def test_disgusted_sentence(self):
        result = emotion_detector("I feel disgusted by this")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sad_sentence(self):
        result = emotion_detector("I am very sad about this")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_watson_400_status_returns_empty_result(self):
        import EmotionDetection.emotion_detection as emotion_module

        class FakeWatsonResponse:
            status_code = 400

            def get_result(self):
                return {"status": 400}

        original = emotion_module._call_watson_api
        emotion_module._call_watson_api = lambda text: FakeWatsonResponse()
        try:
            result = emotion_module.emotion_detector("bad input")
        finally:
            emotion_module._call_watson_api = original

        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
