import { test, expect } from '@playwright/test';

test.describe('EchoWrite Basic Tests', () => {
  test('should load the landing page', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page loads
    await expect(page).toHaveTitle(/EchoWrite/);
    
    // Check for main branding
    await expect(page.getByText('EchoWrite')).toBeVisible();
  });

  test('should display main heading', async ({ page }) => {
    await page.goto('/');
    
    // Check for the main hero text
    await expect(page.getByText('Crafting clarity')).toBeVisible();
    await expect(page.getByText('from the chatter')).toBeVisible();
  });
});
