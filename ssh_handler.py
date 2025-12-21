#!/usr/bin/env python3
"""
SSH Connection Handler
Manages SSH connections and remote command execution
"""

import paramiko
import getpass
import os
import sys
from typing import Optional


class SSHHandler:
    """Handle SSH connections and command execution"""
    
    def __init__(self, hostname: str, username: str, port: int = 22, 
                 key_filename: Optional[str] = None, use_password: bool = False):
        self.hostname = hostname
        self.username = username
        self.port = port
        self.key_filename = key_filename
        self.use_password = use_password
        self.client: Optional[paramiko.SSHClient] = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish SSH connection"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_kwargs = {
                'hostname': self.hostname,
                'username': self.username,
                'port': self.port,
                'timeout': 10,
            }
            
            # Try key-based authentication first
            if self.key_filename:
                if not os.path.exists(self.key_filename):
                    print(f"Warning: Key file {self.key_filename} not found")
                else:
                    connect_kwargs['key_filename'] = self.key_filename
                    print(f"Using key file: {self.key_filename}")
            else:
                # Try default SSH keys
                default_keys = [
                    os.path.expanduser('~/.ssh/id_rsa'),
                    os.path.expanduser('~/.ssh/id_ed25519'),
                    os.path.expanduser('~/.ssh/id_ecdsa'),
                ]
                
                existing_keys = [k for k in default_keys if os.path.exists(k)]
                if existing_keys:
                    print(f"Trying default SSH keys: {', '.join(existing_keys)}")
                    connect_kwargs['key_filename'] = existing_keys
            
            # Password authentication
            if self.use_password:
                password = getpass.getpass(f"Password for {self.username}@{self.hostname}: ")
                connect_kwargs['password'] = password
                connect_kwargs['look_for_keys'] = False
            else:
                # Try key-based auth, fall back to agent
                connect_kwargs['look_for_keys'] = True
                connect_kwargs['allow_agent'] = True
            
            try:
                self.client.connect(**connect_kwargs)
                self.connected = True
                return True
            except paramiko.AuthenticationException:
                if not self.use_password:
                    # Retry with password
                    print("\nKey-based authentication failed. Trying password authentication...")
                    password = getpass.getpass(f"Password for {self.username}@{self.hostname}: ")
                    connect_kwargs['password'] = password
                    connect_kwargs['look_for_keys'] = False
                    connect_kwargs['allow_agent'] = False
                    
                    self.client.connect(**connect_kwargs)
                    self.connected = True
                    return True
                else:
                    raise
                    
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
            return False
        except paramiko.SSHException as e:
            print(f"SSH connection error: {str(e)}")
            return False
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def execute_command(self, command: str, timeout: int = 10) -> str:
        """Execute a command on the remote server and return output"""
        if not self.connected or not self.client:
            raise RuntimeError("Not connected to SSH server")
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            exit_code = stdout.channel.recv_exit_status()
            
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            
            if exit_code != 0 and error:
                raise RuntimeError(f"Command failed: {error}")
            
            return output
            
        except Exception as e:
            raise RuntimeError(f"Command execution failed: {str(e)}")
    
    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            self.connected = False
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
