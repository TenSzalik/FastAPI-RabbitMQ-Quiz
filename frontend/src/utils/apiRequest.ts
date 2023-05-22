const apiRequest = async (url = '', optionsObj: object | null = null, errMsg = null) => {
    // For requests that do not require a response other than an error msg
    try {
        const response = await fetch(url, optionsObj);
        if (!response.ok) throw Error('Please reload the app');
    } catch (err: any | Error) {
        errMsg = err.message;
    } finally {
        return errMsg;
    }
}

export default apiRequest;
