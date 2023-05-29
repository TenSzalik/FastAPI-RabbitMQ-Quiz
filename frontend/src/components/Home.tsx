import apiRequest from "../utils/apiRequest";
import urls from "../utils/apiUrls";

const Home = () => {
  let fetchError: String | null = null;

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
    };
    const request = await apiRequest(url, options);
    fetchError = request;
  };

  const startQuiz = async () => {
    await setCookie();
    await createQueue();
    if (fetchError == null) {
      window.location.replace("/quiz");
    } else {
      alert(
        `Somethink went wrong :( Try again later! Error msg: ${fetchError}`
      );
    }
  };

  return (
    <div>
      <div className="relative h-screen p-4">
        <div className="text-center justify-center p-8 mt-24">
          <h1 className="text-8xl font-bold text-blue-600 tracking-wide">
            Philosophical Compass
          </h1>
          <h2 className="text-4xl font-bold text-amber-100 font-outline-1 tracking-wide p-8">
            Check your philosophical views
          </h2>
          <button
            onClick={startQuiz}
            className="text-4xl text-blue-600 animate-pulse mt-24"
          >
            Ready to play with us?
          </button>
        </div>
        <nav className="flex absolute inset-x-0 bottom-0 items-center space-x-4 justify-evenly p-4">
          <a
            href="http://localhost:8000/redoc"
            className="text-pink-500 font-bold transition-colors duration-300 ease-in-out hover:text-indigo-500"
          >
            API
          </a>
          <a
            href="http://localhost:5173/#about"
            className="text-sky-500 font-bold transition-colors duration-300 ease-in-out hover:text-indigo-500"
          >
            About me
          </a>
          <a
            href="https://github.com/TenSzalik/FastAPI-RabbitMQ-Quiz"
            className="text-green-500 font-bold transition-colors duration-300 ease-in-out hover:text-indigo-500"
          >
            Github
          </a>
        </nav>
      </div>
    </div>
  );
};

export default Home;
