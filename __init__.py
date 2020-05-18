from mycroft.skills.common_query_skill import CommonQuerySkill, CQSMatchLevel


# Dict mapping python members to their age and wether they're alive or dead
PYTHONS = {
    'eric idle': (77, 'alive'),
    'michael palin': (77, 'alive'),
    'john cleese': (80, 'alive'),
    'graham chapman': (48, 'dead'),
    'terry gilliam': (79, 'alive'),
    'terry jones': (77, 'dead')
}


def python_in_utt(utterance):
    """Find a monty python member in the utterance.

    Arguments:
        utterance (str): Sentence to check for Monty Python members
    Returns:
        (str) name of Monty Python member or None
    """
    utterance = utterance.lower()
    for key in PYTHONS:
        if key in utterance:
            # Return the found python
            return key

    # No python found
    return None


def partial_python_in_utt(utterance):
    pass


class PythonAgeSkill(CommonQuerySkill):
    """A Skill for checking the age of the python crew."""

    def format_answer(self, python):
        age, status = PYTHONS[python]
        if status == 'alive':
            return self.dialog_renderer.render('age_alive',
                                               {'person': python, 'age': age})
        else:
            return self.dialog_renderer.render('age_dead',
                                               {'person': python, 'age': age})

    def CQS_match_query_phrase(self, utt):
        """Check the utterance if it is a question we can answer.

        Arguments:
            utt: The question

        Returns: tuple (input utterance, match level, response sentence, extra)
        """
        # Check if sentence contains an age query
        age_query = self.voc_match(utt, 'age')

        # Check if the sentence contains a member of Monty Python
        python = python_in_utt(utt) or partial_python_in_utt(utt)

        # If this is an age query and a monty python member is mentioned the
        # skill can answer this
        if age_query and python:
            if 'monty python' in utt.lower():
                confidence = CQSMatchLevel.EXACT
            else:
                confidence = CQSMatchLevel.CATEGORY
            # return high confidence
            return (utt, confidence, self.format_answer(python))
        else:
            return None


def create_skill():
    return PythonAgeSkill()
