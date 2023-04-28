import { useState, useEffect } from "react";

function Quiz() {
  const [dataQuiz, setDataQuiz] = useState([]);
  const [fetchError, setFetchError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  useEffect(() => {
    const readQuiz = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/quiz/");
        if (!response.ok) throw Error("Did not receive expected data");
        const fetchTasks = await response.json();
        setDataQuiz(fetchTasks);
        setFetchError(null);
      } catch (err: any | Error) {
        setFetchError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    readQuiz();
  }, []);

  function handleAnswerClick(index: Object) {
    setCurrentQuestionIndex(currentQuestionIndex + 1);
    sendToQueue(index);
  }

  const sendToQueue = async (data: Object) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/queue/send/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw Error("Queue doesn't exist");
      setFetchError(null);
    } catch (err: any | Error) {
      setFetchError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const queue: string = document.cookie
    .split(";")
    .find((row) => row.startsWith(" queue="))
    .split("=")[1];

  const generateChart = async () => {
    try {
      setIsLoading(true)
      const response = await fetch("http://127.0.0.1:8000/chart/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ queue: queue }),
      });
      if (!response.ok) throw Error("Something went wrong");
      setFetchError(null);
    } catch (err: any | Error) {
      setFetchError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (currentQuestionIndex >= dataQuiz.length) {
    return (
      <div className="flex items-center justify-center h-screen">
        <button onClick={generateChart}>Zakończ test</button>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center h-screen">
      {isLoading && (
        <p className={"animate-pulse text-pink-500 p-40 text-center"}>
          Loading Items...
        </p>
      )}
      {fetchError && (
        <p
          className={"animate-pulse text-pink-500 p-40 text-center"}
        >{`Error: ${fetchError}`}</p>
      )}
      {!isLoading && (
        <div>
          <div>| {dataQuiz[currentQuestionIndex].category.name} |</div>
          <div>| {dataQuiz[currentQuestionIndex].question.name} |</div>
          {dataQuiz[currentQuestionIndex].answer.map(
            (obj) => (
              (
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
              )
            )
          )}
        </div>
      )}
    </div>
  );
}

export default Quiz;
