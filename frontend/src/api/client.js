const BASE_URL = "http://127.0.0.1:8000"; // change later for production

export const brandScan = async (brand, domain) => {
  const response = await fetch(`${BASE_URL}/brand-risk`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      brand_name: brand,
      domain: domain,
    }),
  });

  if (!response.ok) throw new Error("Brand risk failed");
  return response.json();
};

export const signupRisk = async (email, username) => {
  const response = await fetch(`${BASE_URL}/api/signup-risk`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, username }),
  });

  if (!response.ok) throw new Error("Signup risk failed");
  return response.json();
};