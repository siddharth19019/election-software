import tkinter as tk
from tkinter import ttk, filedialog
from pymongo import MongoClient
from PIL import Image, ImageTk


class VotingSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("School Voting System")
        self.master.geometry("600x500")
        self.db = self.get_database()  # MongoDB database
        self.votes_collection = self.db.votes  # MongoDB collection for votes
        self.credentials = {'user': '123', 'admin': 'VNS2077'}
        self.selected_candidates = {}  # Dictionary to store selected candidates
        self.setup_login_frame()
        self.candidate_images = {}  # Dictionary to store images

    def get_database(self):
        # Provide the Atlas URL, replace username, password, and myFirstDatabase with your information
        CONNECTION_STRING = "mongodb+srv://Votingsoftware:vns150509@votingsoftware.4kaq1jx.mongodb.net/?"

        # Create a connection using MongoClient
        client = MongoClient(CONNECTION_STRING)

        # Create the database
        return client['voting_system']

    def setup_login_frame(self):
        self.login_frame = ttk.Frame(self.master, padding="30 30 30 30")
        self.login_frame.grid(row=0, column=0, sticky="ewns")

        # Add heading
        heading_label = ttk.Label(self.login_frame, text="VIDHYA NIKETAN SCHOOL", font=("Helvetica", 18, "bold"))
        heading_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.login_frame, text="Username:").grid(row=1, column=0, pady=10)
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=10)

        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=10)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.credentials and self.credentials[username] == password:
            if username == 'admin':
                self.show_results()
            else:
                self.setup_frames()
        else:
            self.show_message("Invalid username or password")

    def setup_frames(self):
        self.login_frame.grid_remove()
        self.frames = {}
        positions = ['SPLBoys', 'SPLGirls', 'ASPLBoys', 'ASPLGirls', 'SportsCulturalCaptain', 'House'] + [f'Vote{house}Boys' for house in ['Pandya', 'Pallava', 'Chera', 'Chola']] + [f'Vote{house}Girls' for house in ['Pandya', 'Pallava', 'Chera', 'Chola']]
        for pos in positions:
            frame = ttk.Frame(self.master, padding="30 30 30 30")
            frame.grid(row=0, column=0, sticky="ewns")
            self.frames[pos] = frame

        self.setup_voting('SPLBoys', ['Pranav SK', 'Sanjay Krishna'])
        self.setup_voting('SPLGirls', ['Akshara', 'Geethanjali'])
        self.setup_voting('ASPLBoys', ['Siddharth', 'Nikil'])
        self.setup_voting('ASPLGirls', ['Andrea', 'Medha'])
        self.setup_voting('SportsCulturalCaptain', ['Chinmayi', 'Iniyaa', 'Sandeep'])
        self.setup_house_selection()
        self.setup_house_voting()

        self.show_frame('SPLBoys')

    def setup_voting(self, position, candidates):
        frame = self.frames[position]
        label = ttk.Label(frame, text=f"Vote for {position}")
        label.pack(pady=10)

        for candidate in candidates:
            candidate_frame = ttk.Frame(frame)
            candidate_frame.pack(pady=5)

            image_label = ttk.Label(candidate_frame)
            image_label.pack(side=tk.LEFT, padx=10)
            if (position, candidate) in self.candidate_images:
                image_label.config(image=self.candidate_images[(position, candidate)])
            else:
                btn_browse = ttk.Button(candidate_frame, text="Browse Image",
                                        command=lambda p=position, c=candidate: self.browse_image(p, c))
                btn_browse.pack(side=tk.LEFT, padx=10)

            btn = ttk.Button(candidate_frame, text=f"{candidate}",
                             command=lambda p=position, c=candidate: self.record_vote(p, c))
            btn.pack(side=tk.LEFT, padx=10)

        next_position = self.get_next_position(position)
        next_btn = ttk.Button(frame, text="Next",
                              command=lambda p=position, np=next_position: self.validate_and_next(p, np))
        next_btn.pack(pady=20)

    def browse_image(self, position, candidate):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.candidate_images[(position, candidate)] = photo
            self.setup_frames()  # Refresh the frames to show the image

    def get_next_position(self, current_position):
        positions = ['SPLBoys', 'SPLGirls', 'ASPLBoys', 'ASPLGirls', 'SportsCulturalCaptain', 'House'] + [f'Vote{house}Boys' for house in ['Pandya', 'Pallava', 'Chera', 'Chola']] + [f'Vote{house}Girls' for house in ['Pandya', 'Pallava', 'Chera', 'Chola']]
        current_index = positions.index(current_position)
        return positions[current_index + 1] if current_index + 1 < len(positions) else None

    def setup_house_selection(self):
        frame = self.frames['House']
        label = ttk.Label(frame, text="Select Your House")
        label.pack(pady=10)

        houses = ['Pandya', 'Pallava', 'Chera', 'Chola']
        for house in houses:
            btn = ttk.Button(frame, text=house, command=lambda h=house: self.show_frame(f'Vote{h}Boys'))
            btn.pack(fill='x', pady=5)

    def setup_house_voting(self):
        houses = ['Pandya', 'Pallava', 'Chera', 'Chola']
        house_captains_boys = {
            'Pandya': ['Gautham', 'Vishal'],
            'Pallava': ['Vikram', 'Amit'],
            'Chera': ['Aditya Sidarth', 'Jalambara', 'Pavesh'],
            'Chola': ['Jegan', 'Nithin C S']
        }
        house_captains_girls = {
            'Pandya': ['Jeeva Priya'],
            'Pallava': ['Kavya Mithra', 'Sharvika'],
            'Chera': ['Kartyayani', 'Keerthika', 'Sarvika', 'Shri Vikashini'],
            'Chola': ['Ameliya', 'Dakshina', 'Sahana']
        }
        for house in houses:
            # Boys frame
            frame_boys = self.frames[f'Vote{house}Boys']
            label_boys = ttk.Label(frame_boys, text=f"Vote for {house} House Captain - Boys")
            label_boys.pack(pady=10)

            boys_candidates = house_captains_boys[house]
            for candidate in boys_candidates:
                candidate_frame = ttk.Frame(frame_boys)
                candidate_frame.pack(pady=5)

                image_label = ttk.Label(candidate_frame)
                image_label.pack(side=tk.LEFT, padx=10)
                if (house, candidate) in self.candidate_images:
                    image_label.config(image=self.candidate_images[(house, candidate)])
                else:
                    btn_browse = ttk.Button(candidate_frame, text="Browse Image",
                                            command=lambda h=house, c=candidate: self.browse_image(h, c))
                    btn_browse.pack(side=tk.LEFT, padx=10)

                btn = ttk.Button(candidate_frame, text=f"{candidate}",
                                 command=lambda p=house, c=candidate: self.record_vote(p, c))
                btn.pack(side=tk.LEFT, padx=10)

            next_btn_boys = ttk.Button(frame_boys, text="Next",
                                       command=lambda h=house: self.show_frame(f'Vote{h}Girls'))
            next_btn_boys.pack(pady=20)

            # Girls frame
            frame_girls = self.frames[f'Vote{house}Girls']
            label_girls = ttk.Label(frame_girls, text=f"Vote for {house} House Captain - Girls")
            label_girls.pack(pady=10)

            girls_candidates = house_captains_girls[house]
            for candidate in girls_candidates:
                candidate_frame = ttk.Frame(frame_girls)
                candidate_frame.pack(pady=5)

                image_label = ttk.Label(candidate_frame)
                image_label.pack(side=tk.LEFT, padx=10)
                if (house, candidate) in self.candidate_images:
                    image_label.config(image=self.candidate_images[(house, candidate)])
                else:
                    btn_browse = ttk.Button(candidate_frame, text="Browse Image",
                                            command=lambda h=house, c=candidate: self.browse_image(h, c))
                    btn_browse.pack(side=tk.LEFT, padx=10)

                btn = ttk.Button(candidate_frame, text=f"{candidate}",
                                 command=lambda p=house, c=candidate: self.record_vote(p, c))
                btn.pack(side=tk.LEFT, padx=10)

            finish_btn_girls = ttk.Button(frame_girls, text="Log Out", command=self.logout)
            finish_btn_girls.pack(side=tk.LEFT, pady=20, padx=10)

            add_vote_btn_girls = ttk.Button(frame_girls, text="Add Vote", command=self.setup_frames)
            add_vote_btn_girls.pack(side=tk.LEFT, pady=20, padx=10)

    def record_vote(self, position, candidate):
        self.selected_candidates[position] = candidate
        self.votes_collection.insert_one({"position": position, "candidate": candidate})

    def validate_and_next(self, position, next_position):
        if position in self.selected_candidates:
            if next_position:
                self.show_frame(next_position)
            else:
                self.logout()
        else:
            self.show_message(f"Please select a candidate for {position} before proceeding.")

    def show_message(self, message):
        self.message_label = ttk.Label(self.master, text=message)
        self.message_label.grid(row=1, column=0)

    def show_frame(self, frame_key):
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_key].grid()

    def show_results(self):
        # Create a frame for the results with a scrollbar
        result_container = ttk.Frame(self.master)
        result_container.grid(row=0, column=0, sticky="ewns")

        canvas = tk.Canvas(result_container)
        scrollbar = ttk.Scrollbar(result_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="ewns")
        scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Label(scrollable_frame, text="Voting Results").grid(row=0, column=0, columnspan=2, pady=10)

        positions = ['SPLBoys', 'SPLGirls', 'ASPLBoys', 'ASPLGirls', 'SportsCulturalCaptain', 'Pandya', 'Pallava',
                     'Chera', 'Chola']

        row = 1
        for position in positions:
            ttk.Label(scrollable_frame, text=f"{position}").grid(row=row, column=0, padx=10, pady=5, sticky="w")
            results = list(self.votes_collection.aggregate([
                {"$match": {"position": position}},
                {"$group": {"_id": "$candidate", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}}  # Sort by vote count descending, then candidate ID ascending
            ]))
            if results:
                for result in results:
                    ttk.Label(scrollable_frame, text=f" {result['_id']}").grid(row=row, column=1, padx=10,
                                                                                        pady=5, sticky="w")
                    ttk.Label(scrollable_frame, text=f"{result['count']} votes").grid(row=row, column=2, padx=10,
                                                                                      pady=5, sticky="w")
                    row += 1
            else:
                ttk.Label(scrollable_frame, text="No votes recorded").grid(row=row, column=1, columnspan=2, padx=10,
                                                                           pady=5, sticky="w")
                row += 1

            ttk.Label(scrollable_frame, text="").grid(row=row, column=0, pady=5)  # Add some space between positions
            row += 1

        reset_btn = ttk.Button(scrollable_frame, text="Reset", command=self.reset_votes)
        reset_btn.grid(row=row, column=0, pady=10)

        logout_btn = ttk.Button(scrollable_frame, text="Logout", command=self.setup_login_frame)
        logout_btn.grid(row=row, column=1, pady=10)

        # Expand the result_container to fill the window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        result_container.grid_rowconfigure(0, weight=1)
        result_container.grid_columnconfigure(0, weight=1)

    def reset_votes(self):
        self.votes_collection.delete_many({})
        self.show_message("All votes have been reset")
        self.setup_login_frame()

    def logout(self):
        self.selected_candidates = {}
        self.setup_login_frame()


def main():
    root = tk.Tk()
    app = VotingSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
