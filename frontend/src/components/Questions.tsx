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
    <div className="flex items-center justify-center h-screen">
      {fetchError && (
        <p
          className={"animate-pulse text-pink-500 p-40 text-center"}
        >{`Error: ${fetchError}`}</p>
      )}
      {!fetchError && (
        <div>
          <div>| {dataQuiz[currentQuestionIndex].category.name} |</div>
          <div>| {dataQuiz[currentQuestionIndex].question.name} |</div>
          {dataQuiz[currentQuestionIndex].answer.map((obj) => (
            <li
              key={obj.id}
              onClick={() =>
                handleAnswerClick({
                  queue: queue,
                  category: dataQuiz[currentQuestionIndex].category.name,
                  answer: obj.value,
                })
              }
            >
              {obj.name}
            </li>
          ))}
        </div>
      )}
    </div>
  );
};

export default Questions;
