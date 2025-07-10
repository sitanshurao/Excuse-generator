import sys
import os
from generator import ExcuseGenerator
from proof_generator import ProofGenerator
from emergency_system import EmergencySystem
from apology_generator import ApologyGenerator
from history_manager import HistoryManager
from datetime import datetime
import textwrap

class IntelligentExcuseGenerator:
    def __init__(self):
        self.excuse_gen = ExcuseGenerator()
        self.proof_gen = ProofGenerator()
        self.emergency_sys = EmergencySystem()
        self.apology_gen = ApologyGenerator()
        self.history_mgr = HistoryManager()
        
    def print_header(self, title):
        print("\n" + "="*50)
        print(f"{title:^50}")
        print("="*50)
        
    def print_section(self, title, content, width=70):
        print(f"\n■ {title.upper()} ■")
        print("-"*len(title)*2)
        if isinstance(content, dict):
            for key, value in content.items():
                print(f"  {key.title()}: {value}")
        elif isinstance(content, str):
            for line in textwrap.wrap(content, width=width):
                print(f"  {line}")
        else:
            print(content)
    
    def get_user_choice(self, prompt, options):
        """Get validated user choice from given options"""
        while True:
            print(f"\n{prompt}")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option.capitalize()}")
            
            try:
                choice = int(input("Your choice (1-" + str(len(options)) + "): "))
                if 1 <= choice <= len(options):
                    return options[choice-1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def interactive_mode(self):
        self.print_header("INTELLIGENT EXCUSE GENERATOR")
        
        # Step 1: Select generation type
        gen_type = self.get_user_choice(
            "What would you like to generate?",
            ["excuse", "apology", "proof"]
        )
        
        # Step 2: Select scenario
        scenario = self.get_user_choice(
            "Select scenario:",
            ["work", "business", "school", "social", "family"]
        )
        
        # Step 3: Select tone
        tone = self.get_user_choice(
            "Select tone:",
            ["professional", "casual", "emotional", "urgent"]
        )
        
        # Step 4: Select urgency if relevant
        urgency = "medium"  # default
        if gen_type in ["excuse", "proof"]:
            urgency = self.get_user_choice(
                "Select urgency level:",
                ["low", "medium", "high"]
            )
        
        # Generate the requested content
        if gen_type == "excuse":
            self.generate_excuse(scenario, urgency, tone)
        elif gen_type == "apology":
            self.generate_apology(scenario, tone)
        elif gen_type == "proof":
            self.generate_proof(scenario, urgency, tone)
        
        # Offer to generate more
        if input("\nGenerate something else? (y/n): ").lower() == 'y':
            self.interactive_mode()
        else:
            self.print_header("THANK YOU FOR USING OUR SERVICE")

    def generate_excuse(self, scenario, urgency, tone):
        excuse = self.excuse_gen.generate_excuse(scenario, urgency, tone)
        self.print_section("Generated Excuse", excuse)
        self.history_mgr.add_excuse(excuse, scenario, [tone, urgency])
        
        # Offer to generate proof
        if input("Would you like supporting proof? (y/n): ").lower() == 'y':
            self.generate_proof(scenario, urgency, tone)
        
        # Offer to generate apology
        if input("Would you like an apology message? (y/n): ").lower() == 'y':
            self.generate_apology(scenario, tone)

    def generate_apology(self, scenario, tone):
        apology = self.apology_gen.generate_apology(scenario, tone)
        self.print_section("Generated Apology", apology)
        self.history_mgr.add_excuse(apology, scenario, ["apology", tone])

    def generate_proof(self, scenario, urgency, tone):
        self.print_section("Supporting Evidence", "Generating proof documents...")
        
        doc_proof = self.proof_gen.generate_document(scenario)
        self.print_section("1. Official Document", doc_proof)
        
        location_proof = self.proof_gen.generate_location_log()
        self.print_section("2. Location Verification", location_proof)
        
        chat_img = self.proof_gen.generate_chat_screenshot(
            f"Excuse for {scenario} with {urgency} urgency"
        )
        chat_img.save("chat_proof.png")
        self.print_section("3. Chat Screenshot", "Saved as 'chat_proof.png'")
        
        # Offer emergency simulation for high urgency
        if urgency == "high":
            if input("Simulate emergency contact? (y/n): ").lower() == 'y':
                self.emergency_sys.simulate_emergency_call("Emergency Contact")
                emergency_msg = self.emergency_sys.send_emergency_text(
                    "Family Member", 
                    f"Urgent {scenario} situation"
                )
                self.print_section("Emergency Message Sent", emergency_msg)

def main():
    generator = IntelligentExcuseGenerator()
    
    # Check if user wants to run web server
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        print("Starting web server...")
        print("Web interface will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        # Import and run the web server
        try:
            from web_server import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except ImportError:
            print("Error: web_server.py not found. Please ensure it's in the same directory.")
        except Exception as e:
            print(f"Error starting web server: {e}")
    else:
        # Run in command line mode
        print("Running in command line mode...")
        print("To run web interface, use: python main.py --web")
        generator.interactive_mode()

if __name__ == "__main__":
    main()