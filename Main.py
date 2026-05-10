"""
Quiz App Final Project
By Yashasri Polepally

This project is an interactive quiz website where users answer
trivia questions and receive a final score at the end. The
project was created using Python and Drafter and demonstrates
the use of routes, dataclasses, lists, conditionals, and state.
"""

from dataclasses import dataclass
from drafter import *
from bakery import assert_equal


set_site_information(
    "Yashasri Polepally",
    "A quiz website where users answer questions and get a score.",
    ["My Quiz App Final Project (1).pdf"],
    ["https://docs.google.com/document/d/1jLe7RzqtXbGlDIqs-YEwYGrhfYdRl9zy6DaZrykCCS0/edit?usp=sharing"],
    ["https://ud-s26-cs1.github.io/cs1-website-s26-pyashu-rgb/"],
)
hide_debug_information()
set_website_title("Quiz Application")


@dataclass
class Question:
    """Represent a quiz question with choices and a correct answer. """
    text: str
    options: list[str]
    correct_answer: str


@dataclass
class State:
    """ Stores all changing information for the quiz app. """
    username: str
    score: int
    current_question: int
    questions: list[Question]
    saved_scores: list[int]
    feedback: str
    character: str
    answered_questions: list[Question]


def make_initial_state() -> State:
    """
    Create the starting state for the quiz app.

    Returns:
        The initial State object for the quiz app.
    """
    return State(
        username="",
        score=0,
        character="",
        answered_questions=[],
        current_question=0,
        questions=[
            Question(
                "Leonardo da Vinci's Mona Lisa hangs in what museum?",
                [
                    "The Louvre Museum in Paris",
                    "The British Museum",
                    "The Metropolitan Museum of Art"
                ],
                "The Louvre Museum in Paris"
            ),
            Question(
                "What do you call a group of flamingos?",
                ["A flock", "A flamboyance", "A colony"],
                "A flamboyance"
            ),
            Question(
                "Who is considered the Father of Relativity?",
                ["Isaac Newton", "Albert Einstein", "Galileo Galilei"],
                "Albert Einstein"
            ),
            Question(
                "What is the human body's largest organ?",
                ["The skin", "The liver", "The heart"],
                "The skin"
            ),
            Question(
                "What planet rotates clockwise on its axis?",
                ["Mars", "Venus", "Saturn"],
                "Venus"
            ),
        ],
        saved_scores=[],
        feedback=""
    )


def is_correct_answer(question: Question, answer: str) -> bool:
    """
    Check whether the user's selected answer is correct.

    Args:
        question: The quiz question being answered.
        answer: The answer selected by the user.

    Returns:
        True if the selected answer is correct, otherwise False.
    """
    return answer == question.correct_answer


def quiz_finished(current_question: int,
                  questions: list[Question]) -> bool:
    """
    Check whether the quiz is finished.

    Args:
        current_question: The index of the current question.
        questions: The list of quiz questions.

    Returns:
        True if there are no more questions left, otherwise False.
    """
    return current_question >= len(questions)


def score_message(score: int) -> str:
    """
    Choose the message shown on the results page.

    Args:
        score: The user's final quiz score.

    Returns:
        A message based on the user's score.
    """
    if score == 5:
        return "Amazing job! You got a perfect score!"
    elif score >= 3:
        return "Good job! You passed the quiz."
    else:
        return "Nice try! Review the answers and try again."


@route
def index(state: State) -> Page:
    """
    Show the landing page with name and character selection.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page with name input and character dropdown.
    """
    return Page(state, [
        Header("Welcome to Quiz Application"),
        Text("Enter your name:"),
        TextBox("username", state.username),
        Text("Select a character:"),
        SelectBox("character", ["Cat", "Dog", "Duck"]),
        Button("Continue", welcome_page)
    ])


@route
def welcome_page(state: State, username: str, character: str) -> Page:
    """
    Show the welcome page after the user enters their name and character.

    Args:
        state: The current state of the quiz app.
        username: The name entered by the user.
        character: The character selected by the user.

    Returns:
        A page with welcome message and navigation buttons.
    """
    if username == "":
        return Page(state, [
            Header("Name Required"),
            Text("Please enter your name before continuing."),
            Button("Back", index)
        ])
    state.username = username
    state.character = character
    return Page(state, [
        Text("Begin Quiz App", font_size="14px", font_weight="bold"),
        Text("Welcome " + state.username + " !"),
        Text(
            "This is a short trivia quiz "
            "that you can take and see your score at the end. Good Luck!"
        ),
        Text(" "),
        Button("▶️ Start Quiz", start_quiz_direct),
        Button("🎯 Saved Scores", score_page),
        Button("ℹ️ About", about_page)
    ])


@route
def start_quiz_direct(state: State) -> Page:
    """
    Start the quiz using the previously captured name and character.

    Args:
        state: The current state of the quiz app.

    Returns:
        The first quiz question page.
    """
    state.score = 0
    state.answered_questions = []
    state.current_question = 0
    state.feedback = ""
    return question_page(state)

@route
def start_quiz(state: State) -> Page:
    """
    Display the page where the user enters their name.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page where the user can begin the quiz.
    """
    return Page(state, [
        Header("Start Quiz"),
        Text("Enter your name:"),
        TextBox("username", state.username),

        Text(" "),
        Text("Please Choose a Character Before Starting!"),
        SelectBox(
            "character",
            ["Select a character", "Dog", "Cat", "Duck"]
        ),
        Button("Begin", begin_quiz),
        Button("Home", index)
    ])

def character_icon(character: str) -> str:
    """
    Choose an icon for the selected character.

    Args:
        character: The character selected by the user.

    Returns:
        An emoji icon that matches the selected character.
    """
    if character == "Dog":
        return "🐶"
    elif character == "Cat":
        return "🐱"
    elif character == "Duck":
        return "🦆"
    else:
        return ""

@route
def begin_quiz(state: State, username: str, character: str) -> Page:
    """
    Start the quiz and reset quiz progress.

    Args:
        state: The current state of the quiz app.
        username: The name entered by the user.
        character: The character selected by the user.

    Returns:
        The first quiz question page or an error page
        if no name or character is entered.
    """
    if username == "":
        return Page(state, [
            Header("Name Required"),
            Text("Please enter your name before starting the quiz."),
            Button("Back", start_quiz)
        ])

    if character == "Select a character":
        return Page(state, [
            Header("Character Required"),
            Text("Please choose a character before starting the quiz."),
            Button("Back", start_quiz)
        ])

    state.username = username
    state.character = character
    state.score = 0
    state.answered_questions = []
    state.current_question = 0
    state.feedback = ""

    return question_page(state)


@route
def question_page(state: State) -> Page:
    """
    Display the current quiz question.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page showing the current question and answer choices.
    """

    question = state.questions[state.current_question]
    choices = ["Select an answer"] + question.options

    page_items = [
        Header("Question " + str(state.current_question + 1)),
    ]

    if state.current_question == 0:
        page_items.append(
            Image("question_one.jpg", 420, 250)
        )

    elif state.current_question == 1:
        page_items.append(
            Image("question_two.jpg", 420, 250)
        )

    elif state.current_question == 2:
        page_items.append(
            Image("question_three.jpg", 420, 250)
        )

    elif state.current_question == 3:
        page_items.append(
            Image("question_four.jpg", 420, 250)
        )

    elif state.current_question == 4:
        page_items.append(
            Image("question_five.jpg", 420, 250)
        )

    page_items.extend([
        Text(" "),
        Text(question.text),
        Text(" "),
        SelectBox("answer", choices),
        Button("Submit Answer", submit_answer),
        Button("Home", index),

        Text(" "),
        Text(" "),
        Text(" "),
        Text(" "),
        Text(" "),
    ])

    if state.character == "Dog":
        page_items.append(
            Image("dog_sticker.jpg", 85, 85)
        )

    elif state.character == "Cat":
        page_items.append(
            Image("cat.jpg", 85, 85)
        )

    elif state.character == "Duck":
        page_items.append(
            Image("duck.jpg", 60, 60)
        )

    if state.feedback != "":
        page_items.append(
            Text("*Please choose an answer before submitting.*")
        )

    return Page(state, page_items)


@route
def submit_answer(state: State, answer: str) -> Page:
    """
    Check the submitted answer and update the score.

    Args:
        state: The current state of the quiz app.
        answer: The answer selected by the user.

    Returns:
        The next question page or the final results page.
    """
    question = state.questions[state.current_question]

    if answer == "Select an answer":
        state.feedback = "Please choose an answer before submitting."
        return question_page(state)

    state.answered_questions.append(question)

    if is_correct_answer(question, answer):
        state.score = state.score + 1

    state.feedback = ""
    state.current_question = state.current_question + 1

    if quiz_finished(state.current_question, state.questions):
        state.saved_scores.append(state.score)
        return result_page(state)

    return question_page(state)

@route
def result_page(state: State) -> Page:
    """
    Display the user's final quiz results.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page showing the user's final score and result message.
    """

    message = score_message(state.score)

    page_items = [
        Header("Quiz Finished"),
    ]

    if state.character == "Dog":
        page_items.append(
            Image("dog_sticker.jpg", 90, 90)
        )

    elif state.character == "Cat":
        page_items.append(
            Image("cat.jpg", 90, 90)
        )

    elif state.character == "Duck":
        page_items.append(
            Image("duck.jpg", 65, 65)
        )

    page_items.extend([
        Text("Nice work, " + state.username + "!"),
        Text("Final score: " + str(state.score) + "/5"),
        Text(message),

        Button("Review Answers", review_page),
        Button("Saved Scores", score_page),
        Button("Restart Quiz", start_quiz),
        Button("Home", index)
    ])

    return Page(state, page_items)

@route
def review_page(state: State) -> Page:
    """
    Show all quiz questions and correct answers.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page for reviewing quiz answers.
    """
    review_items = []

    for question_number, question in enumerate(state.questions):
        review_items.append(
            Header("Question " + str(question_number + 1))
        )
        review_items.append(Text(question.text))
        review_items.append(
            Text("Correct Answer: " + question.correct_answer)
        )
        review_items.append(Text(" "))

    return Page(state, [
        Header("📖 Review Answers"),
        *review_items,
        Button("Results", result_page),
        Button("Home", index)
    ])


@route
def score_page(state: State) -> Page:
    """
    Display previously saved quiz scores.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page showing saved quiz scores.
    """
    score_items = []

    for score in state.saved_scores:
        score_items.append(
            Text("Score: " + str(score) + "/5")
        )

    if len(score_items) == 0:
        score_items.append(
            Text("No saved scores yet.")
        )

    return Page(state, [
        Header("Saved Scores"),
        *score_items,
        Button("Home", index)
    ])


@route
def about_page(state: State) -> Page:
    """
    Display information about the quiz website.

    Args:
        state: The current state of the quiz app.

    Returns:
        A page describing the purpose of the project.
    """
    return Page(state, [
        Header("About This Website"),
        Text("Created by Yashasri Polepally"),
        Text(
            "This interactive quiz website allows users to answer "
            "multiple-choice questions, track their score, review "
            "correct answers, and save previous quiz results."
        ),
        Text(
            "The project demonstrates routing, state management, "
            "lists, loops, conditionals, and user interaction."
        ),
        Button("Home", index)
    ])




sample_question = Question(
    "2 + 2?",
    ["3", "4", "5"],
    "4"
)


#Routes are  not unit tested here as they return Page object
initial_state = make_initial_state()
assert_equal(initial_state.score, 0)

assert_equal(is_correct_answer(sample_question, "4"), True)
assert_equal(is_correct_answer(sample_question, "3"), False)

assert_equal(quiz_finished(5, [sample_question] * 5), True)
assert_equal(quiz_finished(2, [sample_question] * 5), False)


assert_equal(score_message(5), "Amazing job! You got a perfect score!")
assert_equal(score_message(3), "Good job! You passed the quiz.")
assert_equal(score_message(1), "Nice try! Review the answers and try again.")

start_server(make_initial_state())
