import http from 'k6/http';
import { fail, check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 1 },
  ],
};

export default function () {
  const url = 'http://localhost:8080/predict';
  const res = http.get(url);
  check(res, { 'status was 200': (r) => r.status == 200 }) || fail(`Request failed with status ${res.status}: ${res.body}`);
}
