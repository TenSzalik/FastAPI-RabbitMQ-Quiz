const QuizForm = ({ endQuiz, inputHandler, inputs }) => {
  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={endQuiz}>
        <fieldset>
          <legend>Age</legend>
          <input
            type="number"
            name="age"
            value={inputs.age || ""}
            onChange={inputHandler}
            className="border-5 border-indigo-500"
          />
          <legend>Sex</legend>
          <div>
            <label htmlFor="F">Female</label>
            <input
              type="radio"
              id="F"
              name="sex"
              value="Female"
              onChange={inputHandler}
            />
            <label htmlFor="M">Male</label>
            <input
              type="radio"
              id="M"
              name="sex"
              value="Male"
              onChange={inputHandler}
            />
          </div>
        </fieldset>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
};

export default QuizForm;
