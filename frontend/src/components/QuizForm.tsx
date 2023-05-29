const QuizForm = ({ endQuiz, inputHandler, inputs }) => {
  return (
    <div className="flex h-screen p-4 border-8 border-dotted border-blue-400">
      <div className="w-1/2 text-center flex items-center justify-center p-8">
        <div className="text-4xl font-bold text-blue-600 leading-relaxed">
          I'm
        </div>
      </div>
      <div className="w-1/2 float-right text-center flex items-center justify-center">
        <form onSubmit={endQuiz} className="p-4">
          <fieldset>
            <div className="p-4">
              <div className=" p-4">
                <span className="text-sm">I'm {inputs.age} years old</span>
                <input
                  className="w-full accent-blue-600"
                  type="range"
                  name="age"
                  value={inputs.age || ""}
                  min="1"
                  max="120"
                  onChange={inputHandler}
                />
              </div>
            </div>
            <div>
              <input
                className="hidden"
                type="radio"
                id="F"
                name="sex"
                value="Female"
                onChange={inputHandler}
              />
              <label
                htmlFor="F"
                className="flex-col p-4 border-2  cursor-pointer"
              >
                Female
              </label>
              <input
                className="hidden"
                type="radio"
                id="M"
                name="sex"
                value="Male"
                onChange={inputHandler}
              />
              <label
                htmlFor="M"
                className="flex-col p-4 border-2  cursor-pointer"
              >
                Male
              </label>
            </div>
          </fieldset>
          <input
            type="submit"
            value="Submit"
            className="font-bold text-blue-600 p-6 cursor-pointer"
          />
        </form>
      </div>
    </div>
  );
};

export default QuizForm;
