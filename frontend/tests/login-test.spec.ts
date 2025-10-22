import { test, expect } from '@playwright/test';

test.describe('EchoWrite Login Test', () => {
  test('should open login modal and test authentication', async ({ page }) => {
    // Navigate to the EchoWrite landing page
    await page.goto('http://localhost:3000');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Take a screenshot to see the current state
    await page.screenshot({ path: 'test-results/landing-page.png', fullPage: true });
    
    // Check if we can see the main branding
    await expect(page.getByText('EchoWrite')).toBeVisible();
    
    // Look for sign in button and click it
    const signInButton = page.getByRole('button', { name: /sign in/i });
    await expect(signInButton).toBeVisible();
    await signInButton.click();
    
    // Wait a moment for modal to appear
    await page.waitForTimeout(1000);
    
    // Take screenshot of modal
    await page.screenshot({ path: 'test-results/auth-modal.png', fullPage: true });
    
    // Check if email field is visible
    const emailField = page.getByLabel('Email');
    await expect(emailField).toBeVisible();
    
    // Check if password field is visible
    const passwordField = page.getByLabel('Password');
    await expect(passwordField).toBeVisible();
    
    // Fill in test credentials (you can modify these)
    await emailField.fill('test@example.com');
    await passwordField.fill('testpassword');
    
    // Take screenshot with filled form
    await page.screenshot({ path: 'test-results/filled-form.png', fullPage: true });
    
    // Look for submit button
    const submitButton = page.getByRole('button', { name: /sign in/i }).last();
    await expect(submitButton).toBeVisible();
    
    // Click submit (this will likely fail since it's a test, but we can see the flow)
    await submitButton.click();
    
    // Wait a moment to see any response
    await page.waitForTimeout(2000);
    
    // Take final screenshot
    await page.screenshot({ path: 'test-results/after-submit.png', fullPage: true });
    
    console.log('Login test completed - check the screenshots in test-results/ folder');
  });
});
