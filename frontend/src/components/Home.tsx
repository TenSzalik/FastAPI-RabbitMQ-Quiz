import apiRequest from "../utils/apiRequest";
import urls from "../utils/apiUrls";

const Home = () => {
  let fetchError: String | null = null
  
  const setCookie = async () => {
    const cookieValue = createUUID4();
    document.cookie = `queue=${cookieValue}`;
  };

  const createUUID4 = () => {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
      (
        c ^
        (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
      ).toString(16)
    );
  };

  const createQueue = async () => {
    const queueCookie = document.cookie
    .split(";")
    .find((row) => row.startsWith(" queue="))
    .split("=")[1];
    const url = urls.queue_create;
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ queue: queueCookie }),
    }
    const request = await apiRequest(url, options);
    fetchError = request;
  };

  const startQuiz = async () => {
      await setCookie();
      await createQueue();
      if (fetchError == null) {
        window.location.replace("/quiz");
      } else {
        alert(`Somethink went wrong :( Try again later! Error msg: ${fetchError}`)
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
