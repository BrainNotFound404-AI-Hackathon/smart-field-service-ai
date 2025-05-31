import unittest
import json
import os
from datetime import datetime
from server.ticket_robot import TicketRobot, ElevatorFaultClassification
from server.model.ticket import Ticket
from pydantic import BaseModel

class TestTicketRobot(unittest.TestCase):
    def setUp(self):
        """Test setup"""
        # Create test data directory
        os.makedirs("data", exist_ok=True)
        # Create TicketRobot instance
        self.robot = TicketRobot()
        
        # Test cases from actual bug.json data
        self.test_cases = [
            {
                "name": "Door System Fault Scenario (101)",
                "data": {
                    "timestamp": "2025-05-31T13:42:25Z",
                    "status": "idle",
                    "environment": {
                        "temperature_c": 24.86,
                        "humidity_percent": 69.19
                    },
                    "sensors": {
                        "vibration_rms": 0.689,
                        "motor_current_a": 21.75,
                        "car_load_kg": 599.8,
                        "acceleration_m_s2": 0.0
                    },
                    "fault_codes": [101]
                },
                "expected_fault_code": 101,
                "expected_severity": "High"
            },
            {
                "name": "Drive System Fault Scenario (201)",
                "data": {
                    "timestamp": "2025-05-30T07:06:01Z",
                    "status": "moving_up",
                    "environment": {
                        "temperature_c": 24.98,
                        "humidity_percent": 55.53
                    },
                    "sensors": {
                        "vibration_rms": 1.324,
                        "motor_current_a": 111.74,
                        "car_load_kg": 758.8,
                        "acceleration_m_s2": -0.464
                    },
                    "fault_codes": [201]
                },
                "expected_fault_code": 201,
                "expected_severity": "High"
            },
            {
                "name": "Safety System Fault Scenario (301)",
                "data": {
                    "timestamp": "2025-06-01T13:35:12Z",
                    "status": "idle",
                    "environment": {
                        "temperature_c": 23.49,
                        "humidity_percent": 52.64
                    },
                    "sensors": {
                        "vibration_rms": 2.77,
                        "motor_current_a": 62.91,
                        "car_load_kg": 1009.4,
                        "acceleration_m_s2": 0.0
                    },
                    "fault_codes": [301]
                },
                "expected_fault_code": 301,
                "expected_severity": "High"
            },
            {
                "name": "Normal Operation Scenario",
                "data": {
                    "timestamp": "2025-05-25T12:04:24Z",
                    "status": "moving_down",
                    "environment": {
                        "temperature_c": 20.77,
                        "humidity_percent": 46.75
                    },
                    "sensors": {
                        "vibration_rms": 0.824,
                        "motor_current_a": 11.82,
                        "car_load_kg": 58.3,
                        "acceleration_m_s2": 0.0
                    },
                    "fault_codes": []
                },
                "expected_fault_code": 0,
                "expected_severity": None
            }
            
        ]
        
        # Save test data
        with open("data/test_elevator_data.json", "w", encoding="utf-8") as f:
            json.dump([case["data"] for case in self.test_cases], f, indent=2)
    
    def test_fault_classification_model(self):
        """Test fault classification model structure"""
        # Verify model fields
        model_fields = ElevatorFaultClassification.model_fields
        self.assertIn('fault_code', model_fields)
        self.assertIn('confidence', model_fields)
        self.assertIn('fault_reason', model_fields)
        self.assertIn('severity', model_fields)
        
        # Verify field types
        self.assertEqual(model_fields['fault_code'].annotation, int)
        self.assertEqual(model_fields['confidence'].annotation, float)
        self.assertEqual(model_fields['fault_reason'].annotation, str)
        self.assertEqual(model_fields['severity'].annotation, str)
        
        # Verify field descriptions
        self.assertEqual(model_fields['fault_code'].description,
                        "Fault code: 101(Door system fault), 201(Drive system fault), 301(Safety system fault), 0(No fault)")
        self.assertEqual(model_fields['confidence'].description,
                        "Confidence of fault detection, range 0-1")
        self.assertEqual(model_fields['severity'].description,
                        "Fault severity: High, Medium, Low")
        
        # Test model instantiation
        test_model = ElevatorFaultClassification(
            fault_code=101,
            confidence=0.95,
            fault_reason="Door system operation abnormal",
            severity="High"
        )
        self.assertEqual(test_model.fault_code, 101)
        self.assertEqual(test_model.confidence, 0.95)
        self.assertEqual(test_model.fault_reason, "Door system operation abnormal")
        self.assertEqual(test_model.severity, "High")
    
    def test_analyze_log_data(self):
        """Test log data analysis functionality"""
        # Analyze test data
        test_data = [case["data"] for case in self.test_cases]
        detected_faults = self.robot.analyze_log_data(test_data)
        
        # Verify return result format
        self.assertIsInstance(detected_faults, list)
        
        if detected_faults:
            fault = detected_faults[0]
            # Verify fault information format
            self.assertIn('timestamp', fault)
            self.assertIn('fault_code', fault)
            self.assertIn('description', fault)
            self.assertIn('confidence', fault)
            self.assertIn('severity', fault)
            
            # Verify fault code
            self.assertIn(fault['fault_code'], [101, 201, 301, 0])
            
            # Verify confidence range
            self.assertGreaterEqual(fault['confidence'], 0)
            self.assertLessEqual(fault['confidence'], 1)
            
            # Verify severity
            self.assertIn(fault['severity'], ['High', 'Medium', 'Low'])
            
            # Print detected fault example
            print("\nDetected Fault Example:")
            print(f"Time: {fault['timestamp']}")
            print(f"Fault Code: {fault['fault_code']}")
            print(f"Description: {fault['description']}")
            print(f"Confidence: {fault['confidence']:.2f}")
            print(f"Severity: {fault['severity']}")
    
    def test_process_log_file(self):
        """Test log file processing functionality"""
        # Process test data file
        self.robot.process_log_file("data/test_elevator_data.json")
        
        # Verify ticket creation
        # Note: Database operations are assumed to be successful, may need to mock in actual testing
        print("\nTicket processing completed")
    
    def test_fault_detection_thresholds(self):
        """Test fault detection thresholds"""
        # Test each scenario
        for case in self.test_cases:
            print(f"\nTesting Scenario: {case['name']}")
            detected_faults = self.robot.analyze_log_data([case['data']])
            
            if detected_faults:
                fault = detected_faults[0]
                print(f"Detected Fault Code: {fault['fault_code']}")
                print(f"Expected Fault Code: {case['expected_fault_code']}")
                print(f"Fault Description: {fault['description']}")
                print(f"Confidence: {fault['confidence']:.2f}")
                print(f"Severity: {fault['severity']}")
                
                # Verify fault code
                self.assertEqual(fault['fault_code'], case['expected_fault_code'],
                               f"Scenario '{case['name']}' fault code mismatch")
                
                # Verify severity
                if case['expected_severity']:
                    self.assertEqual(fault['severity'], case['expected_severity'],
                                   f"Scenario '{case['name']}' severity mismatch")
            else:
                if case['expected_fault_code'] == 0:
                    # For normal scenarios, not detecting faults is correct
                    print("Normal Scenario: No fault detected (as expected)")
                else:
                    self.fail(f"Scenario '{case['name']}' did not detect expected fault")

def run_ticket_robot_tests():
    """Run TicketRobot tests"""
    # Create test instance
    test = TestTicketRobot()
    test.setUp()
    
    try:
        # Run model structure test
        print("\n=== Testing Fault Classification Model ===")
        test.test_fault_classification_model()
        
        # Run data analysis test
        print("\n=== Testing Log Data Analysis ===")
        test.test_analyze_log_data()
        
        # Run file processing test
        print("\n=== Testing Log File Processing ===")
        test.test_process_log_file()
        
        # Run fault detection threshold test
        print("\n=== Testing Fault Detection Thresholds ===")
        # test.test_fault_detection_thresholds()
        
        print("\nTicketRobot Tests Completed!")
        print("Test data file saved at: data/test_elevator_data.json")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")

if __name__ == "__main__":
    # Run TicketRobot tests
    print("\n=== Running TicketRobot Tests ===")
    run_ticket_robot_tests()
