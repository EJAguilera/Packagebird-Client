import grpc
import src.package_operations.PackageOperations_pb2 as PackageOperations_pb2
import src.package_operations.PackageOperations_pb2_grpc as PackageOperations_pb2_grpc

class PackageOperations(object):
    def __init__(self) -> None:
        pass

    def list_packages(self, address, port):
        with grpc.insecure_channel(f'{address}:{port}') as channel:
            stub = PackageOperations_pb2_grpc.PackageOperationServicesStub(channel)
            response = stub.ListPackages(PackageOperations_pb2.PackageListRequest())
            return response
    
    def test_package(self, address, port, packagename):
        with grpc.insecure_channel(f'{address}:{port}') as channel:
            stub = PackageOperations_pb2_grpc.PackageOperationServicesStub(channel)
            request = PackageOperations_pb2.PackageTestRequest(packagename=f'{packagename}')
            response = stub.TestPackage(request)
            return response
    
    def build_package(self, address, port, packagename):
        with grpc.insecure_channel(f'{address}:{port}') as channel:
            stub = PackageOperations_pb2_grpc.PackageOperationServicesStub(channel)
            request = PackageOperations_pb2.PackageBuildRequest(packagename=f'{packagename}')
            response = stub.BuildPackage(request)
            return response
