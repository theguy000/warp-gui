## warp_controller.py
import subprocess
import sys

class WarpController:
    def __init__(self):
        self.warp_cli_path = "warp-cli"  # Default path to the warp-cli executable

    def set_mode(self, mode: str) -> bool:
        """
        Set the Cloudflare WARP client mode.

        :param mode: The mode to set ('doh' for DNS over HTTPS, 'warp+doh' for WARP with DoH)
        :return: True if the operation was successful, False otherwise
        """
        try:
            result = subprocess.run([self.warp_cli_path, 'set-mode', mode], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Error setting mode: {e}", file=sys.stderr)
            return False

    def registration_new(self) -> bool:
        """
        Register a new instance of the Cloudflare WARP client.
        
        :return: True if the operation was successful, False otherwise
        """
        try:
            result = subprocess.run([self.warp_cli_path, 'register'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                with open('registration_status.txt', 'w') as file:
                    file.write('True')
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error registering client: {e}", file=sys.stderr)
            return False

    def connect(self) -> bool:
        """
        Connect the Cloudflare WARP client.
        
        :return: True if the operation was successful, False otherwise
        """
        try:
            result = subprocess.run([self.warp_cli_path, 'connect'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Error connecting client: {e}", file=sys.stderr)
            return False
    def disconnect(self) -> bool:
        """
        Disconnect the Cloudflare WARP client.
        
        :return: True if the operation was successful, False otherwise
        """
        try:
            result = subprocess.run([self.warp_cli_path, 'disconnect'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Error disconnecting client: {e}", file=sys.stderr)
            return False
        
    def check_status(self) -> bool:
        """
        Check the status of the Cloudflare WARP client.
        
        :return: True if WARP is connected, False otherwise
        """
        try:
            result = subprocess.run([self.warp_cli_path, 'status'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode()
            # More precise status check
            if "Connected" in output and "Disconnected" not in output:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error checking status: {e}", file=sys.stderr)
            return False


    def set_license(self, license_key: str) -> bool:
        """
        Set the license key for the Cloudflare WARP client.
        
        :param license_key: The license key to set
        :return: True if the operation was successful, False otherwise
        """
        try:
            result = subprocess.run([self.warp_cli_path, 'set-license', license_key], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Error setting license key: {e}", file=sys.stderr)
            return False
