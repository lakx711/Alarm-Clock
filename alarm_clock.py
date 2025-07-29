import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import datetime
import time
import threading
import os
from pathlib import Path
import pygame
from sound_generator import generate_default_alarm_sound, cleanup_temp_sound

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("🔔 Python Alarm Clock")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Alarm variables
        self.alarms = []
        self.current_alarm = None
        self.alarm_sound = None
        self.snooze_time = 5  # Default snooze time in minutes
        self.is_alarm_playing = False
        self.default_sound_path = None
        
        # Create GUI
        self.create_widgets()
        
        # Start clock update thread
        self.update_clock()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🔔 Python Alarm Clock", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Current time display
        self.time_label = ttk.Label(main_frame, text="", 
                                   font=("Arial", 24, "bold"))
        self.time_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Date display
        self.date_label = ttk.Label(main_frame, text="", 
                                   font=("Arial", 14))
        self.date_label.grid(row=2, column=0, columnspan=3, pady=(0, 30))
        
        # Alarm setting section
        alarm_frame = ttk.LabelFrame(main_frame, text="Set New Alarm", padding="10")
        alarm_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Time input
        ttk.Label(alarm_frame, text="Time (HH:MM):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.time_entry = ttk.Entry(alarm_frame, width=10)
        self.time_entry.grid(row=0, column=1, padx=(0, 20))
        self.time_entry.insert(0, "07:00")
        
        # Sound file selection
        ttk.Label(alarm_frame, text="Sound File:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.sound_var = tk.StringVar(value="Default")
        sound_combo = ttk.Combobox(alarm_frame, textvariable=self.sound_var, 
                                  values=["Default", "Custom File"], width=15)
        sound_combo.grid(row=0, column=3, padx=(0, 10))
        sound_combo.bind("<<ComboboxSelected>>", self.on_sound_selection)
        
        # Browse button
        self.browse_btn = ttk.Button(alarm_frame, text="Browse", 
                                    command=self.browse_sound_file, state="disabled")
        self.browse_btn.grid(row=0, column=4)
        
        # Custom sound file path
        self.sound_path = ""
        
        # Add alarm button
        add_btn = ttk.Button(alarm_frame, text="Add Alarm", 
                            command=self.add_alarm, style="Accent.TButton")
        add_btn.grid(row=1, column=0, columnspan=5, pady=(10, 0))
        
        # Alarms list section
        alarms_frame = ttk.LabelFrame(main_frame, text="Active Alarms", padding="10")
        alarms_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview for alarms
        columns = ("Time", "Sound", "Status")
        self.alarms_tree = ttk.Treeview(alarms_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.alarms_tree.heading(col, text=col)
            self.alarms_tree.column(col, width=150)
        
        self.alarms_tree.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind right-click for context menu
        self.alarms_tree.bind("<Button-3>", self.show_context_menu)
        
        # Scrollbar for alarms list
        scrollbar = ttk.Scrollbar(alarms_frame, orient=tk.VERTICAL, command=self.alarms_tree.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.alarms_tree.configure(yscrollcommand=scrollbar.set)
        
        # Alarm management buttons
        alarm_buttons_frame = ttk.Frame(alarms_frame)
        alarm_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        remove_btn = ttk.Button(alarm_buttons_frame, text="🗑️ Remove Selected", 
                               command=self.remove_alarm, style="Danger.TButton")
        remove_btn.grid(row=0, column=0, padx=(0, 10))
        
        snooze_btn = ttk.Button(alarm_buttons_frame, text="⏰ Snooze Selected", 
                               command=self.snooze_selected_alarm, style="Accent.TButton")
        snooze_btn.grid(row=0, column=1, padx=(0, 10))
        
        test_btn = ttk.Button(alarm_buttons_frame, text="🔔 Test Alarm", 
                             command=self.test_alarm)
        test_btn.grid(row=0, column=2, padx=(0, 10))
        
        clear_all_btn = ttk.Button(alarm_buttons_frame, text="🗑️ Clear All", 
                                  command=self.clear_all_alarms, style="Danger.TButton")
        clear_all_btn.grid(row=0, column=3)
        
        # Snooze settings
        snooze_frame = ttk.LabelFrame(main_frame, text="Snooze Settings", padding="10")
        snooze_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(snooze_frame, text="Snooze Duration (minutes):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.snooze_var = tk.StringVar(value="5")
        snooze_combo = ttk.Combobox(snooze_frame, textvariable=self.snooze_var, 
                                   values=["1", "3", "5", "10", "15"], width=10)
        snooze_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Control buttons
        control_frame = ttk.LabelFrame(main_frame, text="Alarm Controls", padding="10")
        control_frame.grid(row=6, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Stop and Snooze buttons (enabled when alarm is ringing)
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop Alarm", 
                                  command=self.stop_alarm, state="disabled", style="Accent.TButton")
        self.stop_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.snooze_btn = ttk.Button(control_frame, text="⏰ Snooze", 
                                    command=self.snooze_alarm, state="disabled", style="Accent.TButton")
        self.snooze_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Status indicator
        self.alarm_status_label = ttk.Label(control_frame, text="No alarm ringing", 
                                           font=("Arial", 10, "bold"))
        self.alarm_status_label.grid(row=0, column=2, padx=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        alarms_frame.columnconfigure(0, weight=1)
        alarms_frame.rowconfigure(0, weight=1)
        
    def on_sound_selection(self, event=None):
        if self.sound_var.get() == "Custom File":
            self.browse_btn.config(state="normal")
        else:
            self.browse_btn.config(state="disabled")
            self.sound_path = ""
            
    def browse_sound_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Alarm Sound",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.m4a"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.sound_path = file_path
            self.status_var.set(f"Sound file selected: {os.path.basename(file_path)}")
            
    def add_alarm(self):
        time_str = self.time_entry.get().strip()
        
        # Validate time format
        try:
            hour, minute = map(int, time_str.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format (e.g., 07:30)")
            return
            
        # Create alarm time for today
        now = datetime.datetime.now()
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If alarm time has passed today, set it for tomorrow
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)
            
        # Create alarm object
        alarm = {
            'time': alarm_time,
            'sound': self.sound_var.get(),
            'sound_path': self.sound_path,
            'status': 'Active'
        }
        
        self.alarms.append(alarm)
        self.update_alarms_display()
        self.status_var.set(f"Alarm set for {alarm_time.strftime('%H:%M')} on {alarm_time.strftime('%Y-%m-%d')}")
        
    def update_alarms_display(self):
        # Clear existing items
        for item in self.alarms_tree.get_children():
            self.alarms_tree.delete(item)
            
        # Add alarms to treeview
        for i, alarm in enumerate(self.alarms):
            time_str = alarm['time'].strftime('%H:%M')
            sound_str = alarm['sound']
            if alarm['sound'] == "Custom File" and alarm['sound_path']:
                sound_str = os.path.basename(alarm['sound_path'])
            status_str = alarm['status']
            
            self.alarms_tree.insert('', 'end', values=(time_str, sound_str, status_str), tags=(f'alarm_{i}',))
            
    def remove_alarm(self):
        selected = self.alarms_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an alarm to remove")
            return
            
        # Get the index of selected alarm
        item = self.alarms_tree.item(selected[0])
        index = int(item['tags'][0].split('_')[1])
        
        # Check if this is the currently ringing alarm
        removed_alarm = self.alarms[index]
        if self.current_alarm and removed_alarm == self.current_alarm:
            # Stop the audio if this is the ringing alarm
            self.stop_alarm_audio()
            self.current_alarm = None
            self.is_alarm_playing = False
            
            # Disable control buttons
            self.stop_btn.config(state="disabled")
            self.snooze_btn.config(state="disabled")
            self.alarm_status_label.config(text="No alarm ringing", foreground="black")
        
        # Remove alarm
        self.alarms.pop(index)
        self.update_alarms_display()
        self.status_var.set(f"Removed alarm set for {removed_alarm['time'].strftime('%H:%M')}")
        
    def clear_all_alarms(self):
        """Remove all alarms"""
        if not self.alarms:
            messagebox.showinfo("No Alarms", "No alarms to clear")
            return
            
        result = messagebox.askyesno("Clear All Alarms", 
                                   f"Are you sure you want to remove all {len(self.alarms)} alarms?")
        if result:
            # Stop audio if any alarm is ringing
            if self.is_alarm_playing:
                self.stop_alarm_audio()
                self.is_alarm_playing = False
                self.current_alarm = None
                
                # Disable control buttons
                self.stop_btn.config(state="disabled")
                self.snooze_btn.config(state="disabled")
                self.alarm_status_label.config(text="No alarm ringing", foreground="black")
            
            self.alarms.clear()
            self.update_alarms_display()
            self.status_var.set("All alarms cleared")
            
    def test_alarm(self):
        """Test the alarm functionality"""
        if not self.alarms:
            messagebox.showinfo("No Alarms", "Please add an alarm first to test")
            return
            
        # Create a test alarm for 5 seconds from now
        test_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
        test_alarm = {
            'time': test_time,
            'sound': self.sound_var.get(),
            'sound_path': self.sound_path,
            'status': 'Active'
        }
        
        self.alarms.append(test_alarm)
        self.update_alarms_display()
        self.status_var.set(f"Test alarm set for {test_time.strftime('%H:%M:%S')} (5 seconds from now)")
        
        # Show instructions
        messagebox.showinfo("Test Alarm", 
                          "A test alarm has been set for 5 seconds from now.\n\n"
                          "When it goes off, you can:\n"
                          "• Click 'Stop Alarm' to turn it off\n"
                          "• Click 'Snooze' to delay it\n"
                          "• Test the snooze functionality")
        
    def show_context_menu(self, event):
        """Show context menu for alarm management"""
        selected = self.alarms_tree.selection()
        if not selected:
            return
            
        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="🗑️ Remove Alarm", command=self.remove_alarm)
        context_menu.add_command(label="📝 Edit Alarm", command=self.edit_alarm)
        context_menu.add_command(label="⏰ Snooze Alarm", command=self.snooze_selected_alarm)
        context_menu.add_separator()
        context_menu.add_command(label="🔔 Test This Alarm", command=self.test_selected_alarm)
        
        # Show menu at cursor position
        context_menu.tk_popup(event.x_root, event.y_root)
        
    def edit_alarm(self):
        """Edit the selected alarm"""
        selected = self.alarms_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an alarm to edit")
            return
            
        # Get the index of selected alarm
        item = self.alarms_tree.item(selected[0])
        index = int(item['tags'][0].split('_')[1])
        alarm = self.alarms[index]
        
        # Create a simple edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Alarm")
        edit_window.geometry("300x200")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Center the window
        edit_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Time input
        ttk.Label(edit_window, text="New Time (HH:MM):").pack(pady=10)
        time_entry = ttk.Entry(edit_window, width=10)
        time_entry.pack()
        time_entry.insert(0, alarm['time'].strftime('%H:%M'))
        
        def save_changes():
            try:
                time_str = time_entry.get().strip()
                hour, minute = map(int, time_str.split(':'))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError
                    
                # Update alarm time
                now = datetime.datetime.now()
                new_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if new_time <= now:
                    new_time += datetime.timedelta(days=1)
                    
                alarm['time'] = new_time
                self.update_alarms_display()
                self.status_var.set(f"Alarm updated to {new_time.strftime('%H:%M')}")
                edit_window.destroy()
                
            except ValueError:
                messagebox.showerror("Invalid Time", "Please enter time in HH:MM format")
        
        # Save button
        ttk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
        
    def test_selected_alarm(self):
        """Test the selected alarm by setting it to go off in 5 seconds"""
        selected = self.alarms_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an alarm to test")
            return
            
        # Get the index of selected alarm
        item = self.alarms_tree.item(selected[0])
        index = int(item['tags'][0].split('_')[1])
        alarm = self.alarms[index]
        
        # Set alarm to go off in 5 seconds
        alarm['time'] = datetime.datetime.now() + datetime.timedelta(seconds=5)
        alarm['status'] = 'Active'
        
        self.update_alarms_display()
        self.status_var.set(f"Test alarm set for {alarm['time'].strftime('%H:%M:%S')} (5 seconds from now)")
        
        messagebox.showinfo("Test Alarm", 
                          f"Alarm '{alarm['time'].strftime('%H:%M')}' will go off in 5 seconds.\n\n"
                          "You can test the Stop and Snooze functionality.")
        
    def snooze_selected_alarm(self):
        """Snooze the selected alarm by setting it to go off after the snooze duration"""
        selected = self.alarms_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an alarm to snooze")
            return
            
        # Get the index of selected alarm
        item = self.alarms_tree.item(selected[0])
        index = int(item['tags'][0].split('_')[1])
        alarm = self.alarms[index]
        
        # Check if this is the currently ringing alarm
        if self.current_alarm and alarm == self.current_alarm and self.is_alarm_playing:
            # If it's currently ringing, use the existing snooze method
            self.snooze_alarm()
            return
        
        # Calculate snooze time
        snooze_minutes = int(self.snooze_var.get())
        snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze_minutes)
        
        # Update alarm time
        alarm['time'] = snooze_time
        alarm['status'] = 'Active'
        
        # Update display
        self.update_alarms_display()
        self.status_var.set(f"Alarm snoozed for {snooze_minutes} minutes (will ring at {snooze_time.strftime('%H:%M:%S')})")
        
        messagebox.showinfo("Alarm Snoozed", 
                          f"Alarm has been snoozed for {snooze_minutes} minutes.\n\n"
                          f"It will ring again at {snooze_time.strftime('%H:%M:%S')}")
        
    def update_clock(self):
        """Update the clock display every second"""
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        # Check for alarms
        self.check_alarms()
        
        # Schedule next update
        self.root.after(1000, self.update_clock)
        
    def check_alarms(self):
        """Check if any alarms should go off"""
        now = datetime.datetime.now()
        
        for alarm in self.alarms:
            if (alarm['status'] == 'Active' and 
                alarm['time'].hour == now.hour and 
                alarm['time'].minute == now.minute and 
                now.second == 0):
                
                self.trigger_alarm(alarm)
                
    def trigger_alarm(self, alarm):
        """Trigger the alarm"""
        self.current_alarm = alarm
        alarm['status'] = 'Ringing'
        self.is_alarm_playing = True
        
        # Update display
        self.update_alarms_display()
        
        # Show alarm dialog
        self.show_alarm_dialog()
        
        # Play sound in separate thread
        threading.Thread(target=self.play_alarm_sound, daemon=True).start()
        
    def play_alarm_sound(self):
        """Play the alarm sound"""
        try:
            if self.current_alarm['sound'] == "Custom File" and self.current_alarm['sound_path']:
                sound_file = self.current_alarm['sound_path']
            else:
                # Use a simple beep sound (you can replace this with a default sound file)
                sound_file = self.create_default_sound()
                
            if sound_file and os.path.exists(sound_file):
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
            else:
                # Fallback to system beep if no sound file
                self.root.bell()
                
        except Exception as e:
            print(f"Error playing sound: {e}")
            # Fallback to system beep
            self.root.bell()
            
    def create_default_sound(self):
        """Create a simple default sound file"""
        if not self.default_sound_path:
            self.default_sound_path = generate_default_alarm_sound()
        return self.default_sound_path
        
    def show_alarm_dialog(self):
        """Show alarm dialog"""
        # Enable control buttons
        self.stop_btn.config(state="normal")
        self.snooze_btn.config(state="normal")
        
        # Update status label
        self.alarm_status_label.config(text="🔔 ALARM RINGING!", foreground="red")
        
        # Show notification
        messagebox.showinfo("Alarm!", f"Time to wake up!\nAlarm set for {self.current_alarm['time'].strftime('%H:%M')}")
        
    def stop_alarm_audio(self):
        """Stop the alarm audio playback"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"Error stopping audio: {e}")
        
    def stop_alarm(self):
        """Stop the current alarm"""
        # Stop the audio
        self.stop_alarm_audio()
        self.is_alarm_playing = False
            
        if self.current_alarm:
            # Remove the alarm
            if self.current_alarm in self.alarms:
                self.alarms.remove(self.current_alarm)
            self.current_alarm = None
            
        # Disable control buttons
        self.stop_btn.config(state="disabled")
        self.snooze_btn.config(state="disabled")
        
        # Update status label
        self.alarm_status_label.config(text="No alarm ringing", foreground="black")
        
        # Update display
        self.update_alarms_display()
        self.status_var.set("Alarm stopped")
        
    def snooze_alarm(self):
        """Snooze the current alarm"""
        if self.current_alarm and self.is_alarm_playing:
            # Stop current alarm audio
            self.stop_alarm_audio()
            self.is_alarm_playing = False
            
            # Calculate snooze time
            snooze_minutes = int(self.snooze_var.get())
            snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze_minutes)
            
            # Update alarm time
            self.current_alarm['time'] = snooze_time
            self.current_alarm['status'] = 'Active'
            
            # Disable control buttons
            self.stop_btn.config(state="disabled")
            self.snooze_btn.config(state="disabled")
            
            # Update status label
            self.alarm_status_label.config(text="No alarm ringing", foreground="black")
            
            # Update display
            self.update_alarms_display()
            self.status_var.set(f"Alarm snoozed for {snooze_minutes} minutes")
            
            self.current_alarm = None

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create button styles
    style.configure("Accent.TButton", background="#0078d4", foreground="white")
    style.configure("Danger.TButton", background="#dc3545", foreground="white")
    
    app = AlarmClock(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Handle window close
    def on_closing():
        if app.is_alarm_playing:
            app.stop_alarm_audio()
        if app.default_sound_path:
            cleanup_temp_sound(app.default_sound_path)
        pygame.mixer.quit()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main() 