"""Docs."""
import tkinter as tk
from tkinter import TclError, ttk, messagebox

from erlang import ErlangB, ErlangC


class MainGUI(ttk.Frame):  # pylint: disable=too-many-ancestors
    """Docs."""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        master.title("Erlang Calculator")
        master.resizable(0, 0)

        notebook = ttk.Notebook(self)

        erlang_b_frame = ErlangBTab(notebook)
        notebook.add(erlang_b_frame, text=" Erlang B ", padding=10)

        erlang_c_frame = ErlangCTab(notebook)
        notebook.add(erlang_c_frame, text=" Erlang C ", padding=10)

        notebook.grid(row=0, column=0, sticky="nsew")
        self.grid(row=0, column=0, sticky="nsew")


class ErlangBTab(ttk.Frame):  # pylint: disable=too-many-ancestors
    """Docs."""

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # variables
        self.traffic_var = tk.DoubleVar(value=0.0)
        self.channel_var = tk.IntVar(value=0)
        self.block_probality_var = tk.DoubleVar(value=0.0)
        self.option = tk.IntVar(value=2)

        ttk.Label(self, text="").grid(row=0, column=0)

        # erlang field
        erlang_check = ttk.Radiobutton(
            self,
            text="Traffic",
            value=1,
            command=self.__check_btn,
            variable=self.option,
        )
        erlang_check.grid(row=1, column=0, padx=4)

        self.erlang_entry = ttk.Entry(
            self, text="", justify="center", textvariable=self.traffic_var
        )
        self.erlang_entry.grid(row=2, column=0, padx=4)
        # erlang field --> end

        # block field
        block_check = ttk.Radiobutton(
            self,
            text="Block Probability",
            value=2,
            command=self.__check_btn,
            variable=self.option,
        )
        block_check.grid(row=1, column=1, padx=4)
        self.block_probality_entry = ttk.Entry(
            self,
            text="",
            justify="center",
            state="readonly",
            textvariable=self.block_probality_var,
        )
        self.block_probality_entry.grid(row=2, column=1, padx=4)
        # block field --> end

        # channel field
        channel_check = ttk.Radiobutton(
            self,
            text="Channels",
            value=3,
            command=self.__check_btn,
            variable=self.option,
        )
        channel_check.grid(row=1, column=2, padx=4)
        self.channel_entry = ttk.Entry(
            self,
            text="",
            justify="center",
            textvariable=self.channel_var,
        )
        self.channel_entry.grid(row=2, column=2, padx=4)
        # channel field --> end

        ttk.Label(self, text="").grid(row=3, column=0)

        calculate_btn = ttk.Button(
            self,
            text="Calculate",
            command=self.__calculate,
        )
        calculate_btn.grid(row=4, column=1, padx=3)

        ttk.Label(self, text="").grid(row=5, column=0)

    def __check_btn(self) -> None:
        if self.option.get() == 1:
            self.erlang_entry.config(state="readonly")
            self.block_probality_entry.config(state="normal")
            self.channel_entry.config(state="normal")
        elif self.option.get() == 2:
            self.erlang_entry.config(state="normal")
            self.block_probality_entry.config(state="readonly")
            self.channel_entry.config(state="normal")
        elif self.option.get() == 3:
            self.erlang_entry.config(state="normal")
            self.block_probality_entry.config(state="normal")
            self.channel_entry.config(state="readonly")

    def __calculate(self) -> None:
        try:
            prob = self.block_probality_var.get()
            channels = self.channel_var.get()
            traffic = self.traffic_var.get()
            erlang_b = ErlangB(prob, channels, traffic)
            if self.option.get() == 1:
                _traffic = erlang_b.get_traffic()
                self.traffic_var.set(_traffic)
            elif self.option.get() == 2:
                _prob = erlang_b.get_block_prob()
                self.block_probality_var.set(_prob)
            elif self.option.get() == 3:
                _channels = erlang_b.get_n_channels()
                self.channel_var.set(_channels)
        except (TclError, ValueError) as error:
            messagebox.showerror(title="Error", message=str(error))


class ErlangCTab(ttk.Frame):  # pylint: disable=too-many-ancestors
    """Docs."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.call_per_hour_var = tk.DoubleVar(value=0.0)
        self.call_duration_var = tk.DoubleVar(value=0.0)
        self.secs_delay_var = tk.DoubleVar(value=0.0)
        self.message_var = tk.StringVar(value="")

        ttk.Label(self, text="").grid(row=0, column=0)

        # call per hour field
        call_per_hour_label = ttk.Label(self, text="Calls/h")
        call_per_hour_label.grid(row=1, column=0, padx=4)
        call_per_hour_entry = ttk.Entry(
            self,
            text="",
            justify="center",
            textvariable=self.call_per_hour_var,
        )
        call_per_hour_entry.grid(row=2, column=0, padx=4)
        # call per hour field --> end

        # call duration field
        call_duration_label = ttk.Label(self, text="Duration")
        call_duration_label.grid(row=1, column=1, padx=4)
        call_duration_entry = ttk.Entry(
            self, text="", justify="center", textvariable=self.call_duration_var
        )
        call_duration_entry.grid(row=2, column=1, padx=4)
        # call duration field --> end

        # secs delay field
        secs_delay_label = ttk.Label(self, text="Secs Delay")
        secs_delay_label.grid(row=1, column=2, padx=4)
        secs_delay_entry = ttk.Entry(
            self, text="", justify="center", textvariable=self.secs_delay_var
        )
        secs_delay_entry.grid(row=2, column=2, padx=4)
        # secs delay field --> end

        ttk.Label(self, text="").grid(row=3, column=0)

        calculate_btn = ttk.Button(self, text="Calculate", command=self.__calculate)
        calculate_btn.grid(row=4, column=1, padx=3)

        self.message_label = ttk.Label(self, text="", textvariable=self.message_var)
        self.message_label.grid(row=5, column=0, padx=3, columnspan=3)

    def __calculate(self) -> None:
        try:
            call_per_hour = self.call_per_hour_var.get()
            call_duration = self.call_duration_var.get()
            secs_delay = self.secs_delay_var.get()

            erlang_c = ErlangC(call_per_hour, call_duration, secs_delay)

            n_agents, service_level = erlang_c.calc_n_agents()
            self.message_var.set(
                f"N agents: {n_agents}\nService level: {service_level*100}%"
            )
        except (TclError, ValueError) as error:
            messagebox.showerror(title="Error", message=str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    app.mainloop()
