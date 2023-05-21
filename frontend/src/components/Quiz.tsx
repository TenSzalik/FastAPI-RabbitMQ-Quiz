import { useState, useEffect } from "react";

function Quiz() {
  const [dataQuiz, setDataQuiz] = useState([]);
  const [fetchError, setFetchError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [inputs, setInputs] = useState({});
  const [chartHTML, setChartHTML] = useState("");

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

  const inputHandler = (event) => {
    const name: string = event.target.name;
    const value: number = event.target.value;

    setInputs((values) => ({ ...values, [name]: value }));
  };

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

  const deleteQueue = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://127.0.0.1:8000/queue/delete/", {
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

  const generateChart = async (queue_smooth_data: {}) => {
    let data = [{
      type: 'scatterpolar',
      r: Object.values(Object.values(queue_smooth_data)[0]),
      theta: Object.keys(Object.values(queue_smooth_data)[0]),
      fill: 'toself'
    }]

    let layout = {
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
      const response = await fetch("http://127.0.0.1:8000/queue/consume/", {
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
    try {
      setIsLoading(true);
      const response = await fetch("http://127.0.0.1:8000/quiz/result/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ age: age, sex: sex, quiz: quiz }),
      });
      if (!response.ok) throw Error("Something went wrong");
      setFetchError(null);
    } catch (err: any | Error) {
      setFetchError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const endQuiz = async (event) => {
    event.preventDefault();
    await getAnswers();
    console.log(inputs.quiz, inputs);
    console.log({ queue_smooth_data: inputs.quiz });
    await sendResult(inputs.age, inputs.sex, JSON.stringify(inputs.quiz));
    await generateChart({ queue_smooth_data: inputs.quiz });
    await deleteQueue();
    setCurrentQuestionIndex(currentQuestionIndex + 1);
  };

  if (currentQuestionIndex == dataQuiz.length) {
    return (
      <div id="chart" className="flex items-center justify-center h-screen">
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
  }

  if (currentQuestionIndex > dataQuiz.length) {
    console.log("dupa!");
    console.log(typeof chartHTML);
    return (
      <div>
        <div dangerouslySetInnerHTML={{ __html: chartHTML }}></div>
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
}

export default Quiz;
