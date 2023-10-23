const mysql = require('mysql');

const connection = mysql.createConnection({
    host: '127.0.0.1',
    user: 'root',
    password: '1234',
    database: 'detection'
});

connection.query('SELECT * FROM OBJECT_LOG', (error, results, fields) => {
    if (error) {
        console.error('쿼리 실행 중 에러 발생:', error);
        return;
    }
    console.log('쿼리 결과:', results);
});

connection.end((error) => {
    if (error) {
        console.error('연결 종료 중 에러 발생:', error);
        return;
    }
    console.log('MySQL 연결 종료됨');
});
