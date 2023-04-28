function Home() {
  const setCookie = async () => {
    const response = await fetch("http://127.0.0.1:8000/cookie/set/");
    const data = await response.json();
    const cookieValue = data.queue;
    document.cookie = `queue=${cookieValue}`;
  };

  const createQueue = async () => {
    const queueCookie = document.cookie
      .split(";")
      .find((row) => row.startsWith(" queue="))
      .split("=")[1];
    const response = await fetch("http://127.0.0.1:8000/queue/create/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ queue: queueCookie }),
    });
    if (!response.ok) throw Error("SOmethink went wrong");
  };

  const startQuiz = async () => {
    try {
      await setCookie();
      await createQueue();
      window.location.replace("/quiz");
    } catch (error: any | Error) {
      console.log(error);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <button
        onClick={startQuiz}
        className="text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
      >
        Start test
      </button>
    </div>
  );
}

export default Home;
