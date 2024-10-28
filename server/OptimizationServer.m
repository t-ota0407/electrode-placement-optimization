clear;

serverIP = 'localhost';
serverPort = 30002;

optimizationMode = OptimizationMode.SIMPLE_OPTIMIZATION;


try
    tcpipServer = tcpserver(serverPort);
    disp('Waiting for client connection...');

    % Awaiting for the connection to be established
    while ~tcpipServer.Connected
        pause(0.1);
    end
    disp('Client connected');

    while tcpipServer.Connected
        % Receiving data
        if tcpipServer.NumBytesAvailable > 0
            dataReceived = read(tcpipServer, tcpipServer.NumBytesAvailable, "uint8");
            disp(['Received: ', char(dataReceived)]);

            transactions = strsplit(char(dataReceived), ';');

            for i=1:length(transactions)
                transaction = transactions{i};
                if ~isempty(transaction)
                    tokens = strsplit(transaction);
                    instructionType = tokens{1};
                    resourceType = tokens{2};

                    if strcmp(instructionType, 'LOAD')

                        if strcmp(resourceType, 'model')
                            disp('[LOAD model]');

                            modelType = ModelType.fromString(tokens{3});
                            modelPath = modelType.toModelPath(modelType);
                            model = mphopen(modelPath);
                            modelData = mphplot(model,'pg1','rangenum', 1, 'createplot', 'off');
                            jsonBytes = uint8(jsonencode(modelData));

                            sendMessage(tcpipServer, jsonBytes);
                        end
                    
                    elseif strcmp(instructionType, 'SET')

                        if strcmp(resourceType, 'optimization_mode')
                            disp('[SET optimization_mode]');

                            optimizationMode = OptimizationMode.fromString(tokens{3});

                            resultMessage = sprintf('{"optimization_mode": "%s"}', tokens{3});
                            jsonBytes = uint8(jsonencode(resultMessage));

                            sendMessage(tcpipServer, jsonBytes);
                        
                        elseif strcmp(resourceType, 'target_domain')
                            disp('[SET target_domain]');
                            
                            argnum = numel(tokens);
                            if mod(argnum, 2) ~= 0 || argnum < 4
                                error('An invalid number of arguments was provided for [SET target_domain]');
                            end
                            
                            for i = 1:(argnum / 2 - 1)
                                domainArgIdx = 2 * i + 1;
                                thresholdArgIdx = 2 * i + 2;
                                domain = DomainType.fromString(tokens{domainArgIdx});
                                threshold = str2double(tokens{thresholdArgIdx});
                            end
                            
                            resultMessage = sprintf('ok');
                            jsonBytes = uint8(jsonencode(resultMessage));

                            sendMessage(tcpipServer, jsonBytes);
                        
                        elseif strcmp(resourceType, 'conditions')
                            disp('[SET conditions]');
                            
                        end
   
                    
                    elseif strcmp(instructionType, 'RUN')
                        
                        if strcmp(resourceType, 'simulation')
                            disp('[RUN simulation]');

                        end
                    end
                end

            end

            % セミコロンで区切った文字列の配列にパース
            %parsedArray = strsplit(response, ';');

            % ここで受信データを処理する
            %response = ['Echo: ', char(dataReceived)];

            % データの送信
            %write(tcpipServer, uint8(response));
        end

        pause(0.1);  % 0.1秒待機してループを継続
    end
catch ME
    disp(['Error: ', ME.message]);

    disp('Stack trace:');
    for k = 1:length(ME.stack)
        disp(['In ', ME.stack(k).file, ' at line ', num2str(ME.stack(k).line)]);
    end
end

% クリーンアップ
if isvalid(tcpipServer)
    delete(tcpipServer);
    disp('Server closed');
end
