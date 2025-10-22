import { test, expect } from '@playwright/test';
import { config } from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';

// Load environment variables from backend .env file
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
config({ path: path.resolve(__dirname, '../../backend/.env') });

const TEST_EMAIL = process.env.TEST_EMAIL;
const TEST_PASSWORD = process.env.TEST_PASSWORD;

test.describe('EchoWrite Login', () => {
  test('should successfully login with test credentials', async ({ page }) => {
    console.log(`Testing login with email: ${TEST_EMAIL}`);
    
    // Navigate to the landing page
    await page.goto('http://localhost:3000');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Click on "Sign In" button to open the auth modal
    console.log('Clicking Sign In button...');
    await page.getByRole('button', { name: /sign in/i }).first().click();
    
    // Wait for modal to appear
    await page.waitForTimeout(500);
    
    // Fill in the email field
    console.log('Filling email...');
    await page.getByLabel('Email').fill(TEST_EMAIL || '');
    
    // Fill in the password field
    console.log('Filling password...');
    await page.getByLabel('Password').fill(TEST_PASSWORD || '');
    
    // Click the Sign In button in the modal
    console.log('Submitting login form...');
    const submitButtons = page.getByRole('button', { name: /sign in/i });
    await submitButtons.last().click();
    
    // Wait for navigation or response
    await page.waitForTimeout(3000);
    
    // Check if we're redirected to dashboard
    await expect(page).toHaveURL(/dashboard/);
    console.log('✅ Successfully logged in and redirected to dashboard!');
  });
});
