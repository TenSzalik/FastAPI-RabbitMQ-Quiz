import { useState, useEffect } from "react";
import apiRequest from "../utils/apiRequest";
import Questions from "./Questions";
import QuizForm from "./QuizForm";
import urls from "../utils/apiUrls";

const Quiz = () => {
  const [dataQuiz, setDataQuiz] = useState([]);
  const [fetchError, setFetchError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [inputs, setInputs] = useState({});

  useEffect(() => {
    const readQuiz = async () => {
      try {
        const response = await fetch(urls.quiz);
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

  const inputHandler = (event) => {
    const name: string = event.target.name;
    const value: number = event.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
  };

  const queue: string = document.cookie
    .split(";")
    .find((row) => row.startsWith(" queue="))
    .split("=")[1];

  const deleteQueue = async () => {
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ queue: queue }),
    };
    const result = await apiRequest(urls.queue_delete, options);
    if (result) setFetchError(result);
  };

  const generateChart = async (queue_smooth_data: {}) => {
    const data = [
      {
        type: "scatterpolar",
        r: Object.values(Object.values(queue_smooth_data)[0]),
        theta: Object.keys(Object.values(queue_smooth_data)[0]),
        fill: "toself",
      },
    ];
    const layout = {
      autosize: false,
      width: 500,
      height: 500,
      polar: {
        radialaxis: {
          visible: true,
          range: [0, 20],
        },
      },
      showlegend: true,
    };
    Plotly.newPlot("chart", data, layout);
  };

  const getAnswers = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(urls.queue_consume, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ queue: queue }),
      });
      const new_answers = await response.json();
      inputs.quiz = new_answers;
      if (!response.ok) throw Error("Something went wrong");
      setFetchError(null);
    } catch (err: any | Error) {
      setFetchError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const sendResult = async (age: number, sex: string, quiz: string) => {
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ age: age, sex: sex, quiz: quiz }),
    };
    const result = await apiRequest(urls.quiz_result, options);
    if (result) setFetchError(result);
  };

  const endQuiz = async (event) => {
    event.preventDefault();
    setCurrentQuestionIndex(currentQuestionIndex + 1);
    await getAnswers();
    await sendResult(inputs.age, inputs.sex, JSON.stringify(inputs.quiz));
    await generateChart({ queue_smooth_data: inputs.quiz });
    await deleteQueue();
  };

  if (currentQuestionIndex == dataQuiz.length) {
    return <QuizForm endQuiz={endQuiz} inputHandler={inputHandler} inputs={inputs}/>
  }

  if (currentQuestionIndex > dataQuiz.length) {
    return (
      <div
        id="chart"
        className="flex items-center justify-center h-screen"
      ></div>
    );
  }

  return (
    <div>
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
        <Questions
          dataQuiz={dataQuiz}
          currentQuestionIndex={currentQuestionIndex}
          setCurrentQuestionIndex={setCurrentQuestionIndex}
          queue={queue}
        />
      )}
    </div>
  );
};

export default Quiz;
