const request = require('supertest');
const app = require('../../app');

// Mock user information
const userInfo = {
  name: 'John Doe',
  email: 'john.doe@example.com',
  age: 30
};

// Test suite for User Info Form functionality
describe('User Info Form', () => {
  it('should create user info successfully', async () => {
    const response = await request(app)
      .post('/api/user-info')
      .send(userInfo);

    expect(response.statusCode).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.name).toBe(userInfo.name);
    expect(response.body.email).toBe(userInfo.email);
    expect(response.body.age).toBe(userInfo.age);
  });

  it('should fail when required fields are missing', async () => {
    const response = await request(app)
      .post('/api/user-info')
      .send({ email: 'missing.name@example.com' });

    expect(response.statusCode).toBe(400);
    expect(response.body).toHaveProperty('error');
  });

  it('should return user info if user exists', async () => {
    const postResponse = await request(app)
      .post('/api/user-info')
      .send(userInfo);
    const userId = postResponse.body.id;

    const response = await request(app)
      .get(`/api/user-info/${userId}`);

    expect(response.statusCode).toBe(200);
    expect(response.body.name).toBe(userInfo.name);
    expect(response.body.email).toBe(userInfo.email);
    expect(response.body.age).toBe(userInfo.age);
  });

  it('should return 404 if user does not exist', async () => {
    const response = await request(app)
      .get('/api/user-info/nonexistentId');

    expect(response.statusCode).toBe(404);
    expect(response.body).toHaveProperty('error');
  });
});