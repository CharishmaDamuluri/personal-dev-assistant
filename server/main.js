import express from 'express';
import { UserInfoForm } from './components/UserInfoForm';

const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send(renderUserInfoForm());
});

function renderUserInfoForm() {
  return `
    <html>
    <head>
      <title>User Info</title>
    </head>
    <body>
      <div id="app">
        ${UserInfoForm()}
      </div>
    </body>
    </html>
  `;
}

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});