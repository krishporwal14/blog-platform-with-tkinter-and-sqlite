from tkinter import *
import sqlite3

try:
    # Connect to SQLite database
    connection = sqlite3.connect("blog.db")
    cursor = connection.cursor()
    # Create a table 'posts' if it does not exist
    cursor.execute("CREATE TABLE IF NOT EXISTS posts ("
                   "title TEXT, "
                   "content TEXT);")

    # Commit changes to the database
    connection.commit()
except sqlite3.Error as e:
    print(f"Error connecting to SQLite: {e}")

try:
    # Main Tkinter window
    master = Tk()
    master.geometry("500x500")
    master.title("Blog Platform")

    def clear_fields(title_entry=None, content_text=None):
        """Clear the entry and text widget fields."""
        title_entry.delete(0, "end")
        content_text.delete("1.0", "end")

    class UploadBlogWindow(Toplevel):
        def __init__(self, window=None):
            super().__init__(master=window)
            self.geometry("500x500")
            self.title("Upload Blog")

            # Widgets for adding a new blog post
            label1 = Label(self, text="Upload your blog: ", font=("Helvetica", 25))
            label1.pack(side=TOP, pady=30)

            title_label = Label(self, text="Title: ", font=("Helvetica", 15))
            title_label.place(x=90, y=90)
            title_entry = Entry(self, width=30)
            title_entry.place(x=190, y=98)
            self.title_entry = title_entry

            content_label = Label(self, text="Content: ", font=("Helvetica", 15))
            content_label.place(x=90, y=130)
            content_text = Text(self, height=10, width=30)
            content_text.place(x=190, y=128)
            self.content_text = content_text

            submit_btn = Button(self, text="Add Blog", font=("Helvetica", 15), command=self.add_post)
            submit_btn.place(x=200, y=300)

        def add_post(self):
            """Add a new blog post to the database."""
            title = self.title_entry.get()
            content = self.content_text.get("1.0", "end")
            try:
                cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
                connection.commit()
            except sqlite3.Error as e:
                print(f"Sqlite error: {e}")
            clear_fields(self.title_entry, self.content_text)

    class DisplayBlogWindow(Toplevel):
        def on_configure(self, event):
            """Configure the canvas scroll region."""
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def __init__(self, window=None):
            super().__init__(master=window)
            self.geometry("500x500")
            self.title("Display Blogs")
            
            # Widgets to view all blog posts
            label2 = Label(self, text="All Blogs: ", font=("Helvetica", 25))
            label2.pack(side=TOP, pady=30)

            self.canvas = Canvas(self, width=200)
            self.canvas.pack(side="left", fill="y", expand=True)
            scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
            scrollbar.pack(side="right", fill="y")
            self.canvas.configure(yscrollcommand=scrollbar.set)
            self.canvas.bind("<Configure>", self.on_configure)
            self.frame = Frame(self.canvas)
            self.view_post()
            self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        def view_post(self):
            """Display all blog posts."""
            try:
                cursor.execute("SELECT * FROM posts")
            except sqlite3.Error as e:
                print(f"Sqlite error: {e}")
            all_posts = cursor.fetchall()
            for post in all_posts:
                post_title = post[0]
                post_content = post[1]

                # Use Text widget for displaying multiline content
                text_content = Text(self.frame, wrap="word", height=20, width=20)
                text_content.insert("1.0", post_title + "\n" + post_content)
                text_content.configure(state="disabled")  # Make the Text widget read-only
                text_content.pack(pady=10)

                # Add vertical scrollbar
                y_scrollbar = Scrollbar(self.frame, command=text_content.yview)
                y_scrollbar.pack(side="right", fill="y")
                text_content.config(yscrollcommand=y_scrollbar.set)

                # Add horizontal scrollbar
                x_scrollbar = Scrollbar(self.frame, command=text_content.xview, orient="horizontal")
                x_scrollbar.pack(side="bottom", fill="x")
                text_content.config(xscrollcommand=x_scrollbar.set)


    label = Label(master, text="Blog Platform", font=("Helvetica", 25))
    label.pack(side=TOP, pady=30)

    upload_btn = Button(master, text="Upload Blog", font=("Helvetica", 15))
    upload_btn.bind("<Button>", lambda e: UploadBlogWindow(master))
    upload_btn.pack(side=TOP, pady=30)

    display_btn = Button(master, text="View All Blogs", font=("Helvetica", 15))
    display_btn.bind("<Button>", lambda e: DisplayBlogWindow(master))
    display_btn.pack(side=TOP, pady=30)

    master.mainloop()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
