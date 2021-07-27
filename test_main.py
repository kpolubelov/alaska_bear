#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testing REST API application for helping to bears in wild nature.
"""
import pytest
import requests
#import datasets as ds

"""
TODO list:
    - использовать модуль pytest-docker вместо os.popen...
    - конфиг запуска тестов, опции (адреса и пр.)
    - логгирование контейнера
    - убрать все проверки в тестах в отд. функции c возможностью варнингов по таким поводам, например, как Content-Length
    - убрать тела запросов в datasets, и забирать в тесты оттуда. 
        positive_tests = { read_req: {req_data: expected_status_code, expected_result, ... }, create_req.. }
    - добавить тестов
    - поймать Secret Route ;)
    - html report
"""

SERVER = "http://172.17.0.1:8091"

@pytest.mark.usefixtures('task_container')
class Test_Positive_Suite():

    @pytest.mark.docs( "Try get all data from route" )
    def test_get_all_bears( self ) -> None:
        res = requests.get( SERVER + '/bear' )
        assert 200 == res.status_code   # 204 No Content?
        #assert 'application/json;charset=utf8' == res.headers['content-type']
        #assert res.headers['content-length'].isdigit()
        assert [] ==  res.json()

    def test_create_bear( self ) -> None:
        json_data = { "bear_type":"BLACK","bear_name":"MIKHAIL","bear_age":17.5 }
        res = requests.post( SERVER + '/bear', json = json_data )
        assert res.content.isdigit()
        #assert 201 == res.status_code
        global data_id
        data_id = res.content.decode('UTF-8')
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        if res.content == b'EMPTY':
            pytest.fail( f"Unexpected empty in get id: {data_id}" )
        assert json_data  == res.json()
        assert 200 == res.status_code

    def test_update_bear( self ) -> None:
        json_data = { "bear_id": int(data_id), "bear_name":"john" }
        res = requests.put( SERVER + '/bear/' + data_id, json = json_data )
        body = res.content
        assert body == b'OK'
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        assert int( data_id ) == int( res.json()[ 'bear_id' ] )
        if body == b'EMPTY':
            pytest.fail( f"Unexpected empty in record id: {data_id}" )
        #assert 201 == res.status_code

    def test_get_bear( self ) -> None:
        res = requests.get( SERVER + '/bear/' + data_id )
        assert 200 == res.status_code
        #assert json_data == res.json()

    def test_delete_bear( self ) -> None:
        res = requests.delete( SERVER + '/bear/' + data_id )
        assert 200 == res.status_code

    def test_delete_all_bear( self ) -> None:
        res = requests.delete( SERVER + '/bear' )
        assert 200 == res.status_code

    def test_get_all_bears( self ) -> None:
        res = requests.get( SERVER + '/bear' )
        assert 200 == res.status_code 
        assert [] ==  res.json()


#@pytest.mark.skip()
@pytest.mark.usefixtures('task_container')
class Test_Negative_Suite():

    @pytest.mark.docs( "Try request with incorrect bear_type data: lowercase" )
    def test_create_incorrect_bear_type( self ) -> None:
        json_data = {"bear_type":"black","bear_name":"mikhail","bear_age":17.5}
        res = requests.post( SERVER + '/bear', json = json_data )
        assert ( res.status_code in ( 400,  404 ) )
        assert res.content.isdigit()
        data_id = res.content.decode('UTF-8')
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        assert json_data  == res.json()

    @pytest.mark.docs( "Try request with GUMMY bear_type" )
    def test_create_gummy_bear_type( self ) -> None:
        json_data = {"bear_type":"GUMMY","bear_name":"Bob","bear_age":43}
        res = requests.post( SERVER + '/bear', json = json_data )
        assert res.status_code == 200
        assert res.content.isdigit()
        data_id = res.content.decode('UTF-8')
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        assert json_data  == res.json()

    @pytest.mark.docs( "Try request with incorrect data format: as http instead json" )
    def test_create_incorrect_post( self ) -> None:
        json_data = {"bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5}
        res = requests.post( SERVER + '/bear', data = json_data )
        assert ( res.status_code in ( 400,  404 ) )
        assert res.content.isdigit()
        data_id = res.content.decode('UTF-8')
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        assert json_data  == res.json()

    @pytest.mark.docs( "Try update nonexistent data" )
    def test_update_nonexistent_bear( self ) -> None:
        json_data = { "bear_name":"MIKHAIL" }
        data_id = '404'
        res = requests.put( SERVER + '/bear/' + data_id, json = json_data )
        assert ( res.status_code in [ 400, 404 ] )
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        assert json_data in res.json()

    @pytest.mark.docs( "Forced upper case bear_name" )
    def test_create_variative_name_bear( self ) -> None:
        json_data = { "bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5 }
        res = requests.post( SERVER + '/bear', json = json_data )
        assert res.content.isdigit()
        #assert 201 == res.status_code
        global data_id
        data_id = res.content.decode('UTF-8')
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        if res.content == b'EMPTY':
            pytest.fail( f"Unexpected empty in get id: {data_id}" )
        assert json_data  == res.json()
        assert 200 == res.status_code

    def test_create_very_old_bear( self ) -> None:
        json_data = { "bear_type":"BLACK","bear_name":"MIKHAIL","bear_age":128 }
        res = requests.post( SERVER + '/bear', json = json_data )
        assert res.content.isdigit()
        #assert 201 == res.status_code
        global data_id
        data_id = res.content.decode('UTF-8')
        res = requests.get( SERVER + '/bear/' + data_id )
        json_data.update( { 'bear_id': int( data_id ) } )
        if res.content == b'EMPTY':
            pytest.fail( f"Unexpected empty in get id: {data_id}" )
        assert json_data  == res.json()
        assert 200 == res.status_code


#@pytest.mark.skip()
@pytest.mark.usefixtures('task_container')
class Test_Vulnerability_suite():

    def test_primitive_path_traversal( self ) -> None:

        # TODO
        # FIXME
        http_style_pt = '%2E%2E/etc/passwd', '%2E%2E/%2E%2E/etc/passwd', '%2E%2E/%2E%2E/%2E%2E/etc/passwd', '%2E%2E/%2E%2E/%2E%2E/%2E%2E/%2E%2E/etc/passwd'
        pt = '../etc/passwd', '../../etc/passwd', '../../../etc/passwd', '../../../../../etc/passwd'
        for entity in pt:
            res = requests.get( SERVER + '/info/' + entity )
            assert ( res.status_code in [ 400, 404 ] )
            res = requests.get( SERVER + '/bear/' + entity )
            assert ( res.status_code in [ 400, 404 ] )

        for entity in http_style_pt:
            res = requests.get( SERVER + '/info/' + entity )
            assert ( res.status_code in [ 400, 404 ] )
            res = requests.get( SERVER + '/bear/' + entity )
            assert ( res.status_code in [ 400, 404 ] )
