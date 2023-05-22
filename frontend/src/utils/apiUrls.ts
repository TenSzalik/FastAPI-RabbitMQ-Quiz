const host = 'http://127.0.0.1:8000/'

const urls = {
    quiz: host + 'quiz/',
    quiz_result: host + 'quiz/result/',
    queue_create: host + 'queue/create/',
    queue_send: host + 'queue/send/',
    queue_delete: host + 'queue/delete/',
    queue_consume: host + 'queue/consume/'
}

export default urls;
