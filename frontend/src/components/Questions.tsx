import { useState } from "react";
import apiRequest from "../utils/apiRequest";
import urls from "../utils/apiUrls";

const Questions = ({
  dataQuiz,
  currentQuestionIndex,
  setCurrentQuestionIndex,
  queue,
}) => {
  const [fetchError, setFetchError] = useState(null);

  const handleAnswerClick = (index: Object) => {
    setCurrentQuestionIndex(currentQuestionIndex + 1);
    sendToQueue(index);
  };

  const sendToQueue = async (data: Object) => {
    const url = urls.queue_send;
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };
    const result = await apiRequest(url, options);
    if (result) setFetchError(result);
  };

  return (
    <div className="h-screen p-4 border-8 border-dotted border-blue-400">
      {fetchError && (
        <p
          className={"animate-pulse text-pink-500 p-40 text-center"}
        >{`Error: ${fetchError}`}</p>
      )}
      {!fetchError && (
        <div className="flex">
          <div className="w-1/2 text-center justify-center p-8">
            <div className="text-x text-blue-600">
              {dataQuiz[currentQuestionIndex].category.name}
            </div>
            <div className="text-4xl font-bold text-blue-600 leading-relaxed">
              {dataQuiz[currentQuestionIndex].question.name}
            </div>
            <div className="text-2xl text-blue-600 mt-12">
              What do you think?
            </div>
            <div className="absolute inset-x-12 bottom-12 border-4 border-dotted rounded-full bg-blue-600 w-36 h-36 flex justify-center items-center text-center p-5 shadow-xl">
              <span className="text-4xl font-bold text-white ">
                {currentQuestionIndex + 1}/{dataQuiz.length}
              </span>
            </div>
          </div>
          <div className="w-1/2 float-right text-center justify-center p-8">
            {dataQuiz[currentQuestionIndex].answer.map((obj) => (
              <div
                key={obj.id}
                onClick={() =>
                  handleAnswerClick({
                    queue: queue,
                    category: dataQuiz[currentQuestionIndex].category.name,
                    answer: obj.value,
                  })
                }
                className="font-bold max-w-lg text-2xl justify-center text-center hover:text-blue-600 duration-300 transition cursor-pointer"
              >
                {obj.id == dataQuiz[currentQuestionIndex].answer[0].id && (
                  <div className="flex items-center justify-center border-yellow-400 text-yellow-400 border-2 border-blue-600 rounded-t-full hover:bg-yellow-400 hover:text-blue-400 duration-300 h-64">
                    {obj.name}
                  </div>
                )}
                {obj.id ==
                  dataQuiz[currentQuestionIndex].answer[
                    dataQuiz[currentQuestionIndex].answer.length - 1
                  ].id && (
                  <div className="flex items-center justify-center border-sky-400 text-sky-400 border-2 rounded-b-full hover:bg-sky-400 hover:text-white duration-300 h-64">
                    {obj.name}
                  </div>
                )}
                {obj.id > dataQuiz[currentQuestionIndex].answer[0].id &&
                  obj.id <
                    dataQuiz[currentQuestionIndex].answer[
                      dataQuiz[currentQuestionIndex].answer.length - 1
                    ].id && (
                    <div className="flex items-center justify-center border-blue-400 text-blue-400 border-l-2 border-r-2 hover:bg-blue-400 hover:text-white duration-300 h-12">
                      {obj.name}
                    </div>
                  )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Questions;
