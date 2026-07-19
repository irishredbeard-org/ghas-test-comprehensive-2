module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/typescript/**/*.test.ts'],
  transform: { '^.+\\.ts$': ['ts-jest', { diagnostics: false }] }
};
