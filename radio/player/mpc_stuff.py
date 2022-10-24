import subprocess as sp


class MpdPlayer:
    def add_track(self, track):
        sp.run(["mpc", "add", track], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        sp.run(["mpc", "play"], stdout=sp.PIPE, stderr=sp.PIPE)

    def clear_playlist(self):
        sp.run(["mpc", "clear"], stdout=sp.PIPE, stderr=sp.PIPE)
