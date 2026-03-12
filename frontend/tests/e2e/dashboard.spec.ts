import { expect, test } from "@playwright/test";

test("dashboard renders core workflow copy", async ({ page }) => {
  await page.goto("/dashboard");
  await expect(page.getByRole("heading", { name: "Turn parcel IDs into lawful diligence records" })).toBeVisible();
  await expect(page.getByText("Legal disclaimer")).toBeVisible();
  await expect(page.getByRole("link", { name: "Bulk import parcels" })).toBeVisible();
});

