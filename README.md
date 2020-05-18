# Common query skills

The common query skill system is lead by the fallback_query skill. This skill handles queries matching a question pattern such as "What is the height of the Eiffle Tower" and "When is lunch". A matched question will be sent to all skills based upon the `CommonQuerySkill` base class. The skills will return wether they can answer the query along with an answer when applicable. The "best" match will be selected and spoken to the user.

## CommonQuerySkill

A skill interfacing with the common query framework inherits from the the `CommonQuerySkill` and needs to define a method `CQS_match_query_phrase()` taking an utterance as argument.


The general structure is:

```python
from mycroft.skills.common_query_skill import CommonQuerySkill, CQSMatchLevel

class MyCommonQuerySkill(CommonQuerySkill):
    def CQS_match_query_phrase(self, utt):
       # Parsing implementation
       # [...]
       return (utt, CQSMatchLevel.LEVEL, answer_string)

def create_skill():
    return MyCommonQuerySkill()
```

The `CQS_match_query_phrase()` method will parse the utterance and determine if it can handle the query. if it can't answer it will return `None` and if it _can_ answer it will return a data tuple with the format

```python
((str)Input Query, CQSMatchLevel, (str)Answer Text)
```

The input query is returned to map the query to the answer.

CQSMatchLevel is an Enum with the possible values


- `CQSMatchLevel.EXACT`: The skill is very confident that it has the precise answer the user is looking for. Category match and a known entity is referenced.
- `CQSMatchLevel.CATEGORY`: The skill could determine that the type of question matches a category that the skill is good at finding.
- `CQSMatchLevel.GENERAL`: This skill tries to answer all questions and found an answer. 


## An Example

Let's make a simple skill that tells us the age of the various Monty Python members. A quick draft looks like this


```python
from mycroft.skills.common_query_skill import CommonQuerySkill, CQSMatchLevel

                                                                                
                                                                                
# Dict mapping python members to their age and wether they're alive or dead     
PYTHONS = {
    'eric idle': (77,'alive'),
    'michael palin': (77, 'alive'),
    'john cleese': (80, 'alive'),
    'graham chapman': (48, 'dead'),
    'terry gilliam': (79, 'alive'),
    'terry jones': (77, 'dead')
}


def python_in_utt(utterance):
    """Check if one of the members of monty python
    for key in PYTHONS:
        if key in utterance.lower():
            # Return the found python
            return key

    # No python found
    return None


class PythonAgeSkill(CommonQuerySkill):
    """A Skill for checking the age of the python crew."""

    def format_answer(self, python):
        """Create string with answer for the specified "python" person."""
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
        # Check if this is an age query
        age_query = self.voc_match(utt, 'age')

        # Check if a monty python member is mentioned
        python = full_python_in_utt(utt)

        # If this is an age query and a monty python member is mentioned the
        # skill can answer this
        if age_query and python:
            # return high confidence
            return (utt, CQSMatchLevel.CATEGORY, self.format_answer(python))
        else:
            return None


def create_skill():
    return PythonAgeSkill()
```


As seen above the `CQS_match_query_phrase()` checks if this is an age related utterance and if the utterance contains the name of a Monty Python member. If both criterias are met it returns a match with a `CQSMatchLevel.CATEGORY` confidence together with a rendereded dialog with the answer.

If both criterias aren't fulfilled the method will return None indicating that it can't answer the query.

This will be able to provide answers to queries such as

`how old is Eric Idle`

"what's Eric Idle's age

To make this more exact we can add support for checking for the words "monty python", and if present return the highest confidence

The method for parsing the example is quite simplistic but there are many different toolkits out there for doing the question parsing. [Adapt](https://pypi.org/project/adapt-parser/), [little questions](https://pypi.org/project/little-questions/), [padaos](https://pypi.org/project/padaos/) and may more!
