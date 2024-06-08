from ec2_metadata import ec2_metadata

def get_ec2_metadata():
    print(f"Public IPv4: {ec2_metadata.public_ipv4}")
    print(f"Region: {ec2_metadata.region}")
    print(f"Availability Zone: {ec2_metadata.availability_zone}")
    
    #print(f"Hostname: {ec2_metadata.hostname}")

if __name__ == "__main__":
    get_ec2_metadata()

