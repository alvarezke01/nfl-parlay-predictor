from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from parlays.models import Parlay, ParlayLeg


class ParlayCreateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("parlay-create")

    def test_create_parlay_success(self):
        """Test successful parlay creation with valid data"""
        data = {
            "stake": 25.0,
            "legs": [
                {"model_prob": 0.65, "market_odds_american": -120},
                {"model_prob": 0.58, "market_odds_american": -110},
                {"model_prob": 0.35, "market_odds_american": 180}
            ]
        }

        response = self.client.post(self.url, data, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response data structure
        response_data = response.data
        self.assertIn("id", response_data)
        self.assertIn("legs", response_data)
        self.assertEqual(response_data["stake"], 25.0)
        self.assertEqual(response_data["source"], "user")
        self.assertIsNotNone(response_data["combined_probability"])
        self.assertIsNotNone(response_data["expected_value"])
        self.assertIsNotNone(response_data["fair_odds_american"])
        self.assertIsNotNone(response_data["market_parlay_odds_american"])

        # Check that legs are included
        self.assertEqual(len(response_data["legs"]), 3)
        for leg in response_data["legs"]:
            self.assertIn("model_prob", leg)
            self.assertIn("market_odds_american", leg)
            self.assertIn("leg_ev_at_1u", leg)

        # Assert database records
        self.assertEqual(Parlay.objects.count(), 1)
        self.assertEqual(ParlayLeg.objects.count(), 3)

        parlay = Parlay.objects.first()
        self.assertEqual(parlay.stake, 25.0)
        self.assertEqual(parlay.source, "user")
        self.assertIsNotNone(parlay.combined_probability)
        self.assertIsNotNone(parlay.expected_value)

        legs = ParlayLeg.objects.filter(parlay=parlay)
        self.assertEqual(legs.count(), 3)
        
        # Check first leg
        leg1 = legs[0]
        self.assertEqual(leg1.model_prob, 0.65)
        self.assertEqual(leg1.market_odds_american, -120)
        self.assertIsNotNone(leg1.leg_ev_at_1u)

    def test_create_parlay_empty_legs(self):
        """Test parlay creation with empty legs should fail"""
        data = {
            "stake": 10.0,
            "legs": []
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_parlay_invalid_probability(self):
        """Test parlay creation with invalid probability should fail"""
        data = {
            "stake": 10.0,
            "legs": [
                {"model_prob": 1.5, "market_odds_american": -110}  # > 1.0
            ]
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_parlay_negative_stake(self):
        """Test parlay creation with negative stake should fail"""
        data = {
            "stake": -10.0,
            "legs": [
                {"model_prob": 0.6, "market_odds_american": -110}
            ]
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
